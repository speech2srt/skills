"""Stage 2: Denoise (L4 GPU) - Speech enhancement."""

import io
import sys
from pathlib import Path

import src.config as config
import src.images as images


@images.app.function(
    image=images.image_denoise,
    gpu=config.GPU_TYPE,
    volumes={
        config.MOUNT_DATA: images.volume_data,
        config.MOUNT_MODELS: images.volume_models,
    },
    timeout=config.TIMEOUT_DENOISE,
)
def denoise(path: str) -> list[dict]:
    """Enhance .flac files in /mnt/data/<path>/input, output to /mnt/data/<path>/output."""
    import soundfile as sf
    from clearvoice import ClearVoice

    # ============================================================
    # Model initialization (runs once on cold start)
    # ============================================================

    # ClearVoice library reads model files from /root/checkpoints by default,
    # but actual model files are stored in volume_models at /checkpoints.
    # Create a symlink /root/checkpoints -> /mnt/models/checkpoints
    # so the library can locate the models correctly.
    MODELS_DIR = Path(config.MOUNT_MODELS)
    CHECKPOINTS_DIR = MODELS_DIR / "checkpoints"
    workdir_checkpoints = Path("/root/checkpoints")

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    if not workdir_checkpoints.exists() or not workdir_checkpoints.is_symlink():
        workdir_checkpoints.parent.mkdir(parents=True, exist_ok=True)
        if workdir_checkpoints.exists():
            workdir_checkpoints.rmdir()
        workdir_checkpoints.symlink_to(CHECKPOINTS_DIR)

    CHECKPOINTS_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("ClearVoice MossFormer2_SE_48K")
    print("=" * 60)

    # Check checkpoints cache size to verify models are downloaded
    print("\n[1] Checkpoints cache")
    if CHECKPOINTS_DIR.exists():
        total_size = sum(
            f.stat().st_size for f in CHECKPOINTS_DIR.rglob("*") if f.is_file()
        )
        print(f"    Cache size: {total_size / (1024 * 1024):.2f} MB")
    else:
        print("    Cache directory empty")

    # Initialize ClearVoice model (first call downloads models to checkpoints)
    print("\n[2] Initializing model...")
    myClearVoice = ClearVoice(
        task="speech_enhancement", model_names=["MossFormer2_SE_48K"]
    )
    print("    Model loaded!")

    # ============================================================
    # Scan input directory
    # ============================================================
    input_dir = Path(config.MOUNT_DATA) / path / config.DIR_INPUT

    print(f"\n[3] Scanning: {input_dir}")
    if not input_dir.exists():
        print("    Input directory does not exist")
        return []

    flac_files = sorted(input_dir.glob(f"*{config.FLAC_EXTENSION}"))
    print(f"    Found {len(flac_files)} .flac files")

    if not flac_files:
        print("    No .flac files found, skipping denoise stage")
        return []

    # Ensure output directory exists
    output_dir = Path(config.MOUNT_DATA) / path / config.DIR_OUTPUT
    output_dir.mkdir(parents=True, exist_ok=True)

    # ============================================================
    # Process each audio file
    # ============================================================
    print(f"\n[4] Processing {len(flac_files)} files...")
    results = []
    for flac_file in flac_files:
        output_path = output_dir / f"{flac_file.stem}{config.ENHANCED_SUFFIX}"

        print(f"\n    Processing: {flac_file.name} -> {output_path.name}")

        file_size = flac_file.stat().st_size / (1024 * 1024)
        print(f"        Input: {flac_file.name} ({file_size:.2f} MB)")

        print("        Enhancing...")
        sys.stdout.flush()

        output_wav = myClearVoice(input_path=str(flac_file), online_write=False)
        print("        Done!")

        # Write enhanced audio to Volume (convert to bytes via BytesIO)
        # ClearVoice may return audio with shape (channels, samples) or (samples, channels);
        # ensure output is (samples, channels) before writing.
        if output_wav.ndim == config.AUDIO_STEREO_NDIM:
            output_wav = output_wav.T

        buffer = io.BytesIO()
        sf.write(
            buffer,
            output_wav,
            samplerate=config.AUDIO_SAMPLE_RATE,
            subtype=config.AUDIO_SUBTYPE,
            format=config.AUDIO_FORMAT,
        )
        buffer.seek(0)
        output_path.write_bytes(buffer.getvalue())

        output_size = output_path.stat().st_size / (1024 * 1024)
        print(f"        Output: {output_path.name} ({output_size:.2f} MB)")

        results.append(
            {
                "input": flac_file.name,
                "output": output_path.name,
                "input_size_mb": round(file_size, 2),
                "output_size_mb": round(output_size, 2),
            }
        )

    # Commit all changes to volume_data
    images.volume_data.commit()

    print(f"\n{'=' * 60}")
    print(f"DENOISE COMPLETE. Processed {len(results)} files")
    print("=" * 60)

    return results
