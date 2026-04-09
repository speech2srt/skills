"""
Modal service: Vocal isolation (source separation) pipeline.

ffmpeg conversion (CPU) and Demucs model loading (GPU) run in parallel via ThreadPoolExecutor.
GPU inference then processes each .flac file sequentially.

Usage:
    modal run isolate.py --slug <slug>
"""

import concurrent.futures
import io
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

import src.config as config
import src.images as images


def _run_ffmpeg(
    upload_dir: Path, intermediate_dir: Path
) -> tuple[list[dict], list[str]]:
    """
    Convert all audio/video files in upload/ to 48kHz .flac.
    Output goes to /tmp/speech2srt-isolate/<slug>/.
    Runs in ThreadPool. Returns (results, log_lines).
    """
    intermediate_dir.mkdir(parents=True, exist_ok=True)
    log_lines: list[str] = []
    results: list[dict] = []

    upload_files = sorted(f for f in upload_dir.iterdir() if f.is_file())
    if not upload_files:
        return results, log_lines

    for upload_file in upload_files:
        probe_cmd = [
            "ffprobe",
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_streams",
            "-show_format",
            str(upload_file),
        ]
        audio_duration = 0.0
        try:
            probe_result = subprocess.run(
                probe_cmd,
                capture_output=True,
                text=True,
                timeout=config.FFPROBE_TIMEOUT,
            )
            data = json.loads(probe_result.stdout)
            streams = data.get("streams", [])
            has_audio = any(s.get("codec_type") == "audio" for s in streams)
            if has_audio:
                audio_duration = float(data.get("format", {}).get("duration", 0))
        except Exception:
            has_audio = False

        if not has_audio:
            log_lines.append(f"  {upload_file.name}  [skip - no audio]")
            continue

        output_file = intermediate_dir / f"{upload_file.stem}{config.FLAC_EXTENSION}"

        ffmpeg_cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(upload_file),
            "-vn",
            "-acodec",
            "flac",
            "-ar",
            str(config.AUDIO_SAMPLE_RATE),
            "-ac",
            str(config.AUDIO_CHANNELS),
            str(output_file),
        ]

        conv_t0 = time.monotonic()
        subprocess.run(
            ffmpeg_cmd,
            capture_output=True,
            text=True,
            timeout=config.FFMPEG_TIMEOUT,
            check=True,
        )
        conv_elapsed = time.monotonic() - conv_t0
        input_size_mb = upload_file.stat().st_size / (1024 * 1024)
        output_size_mb = output_file.stat().st_size / (1024 * 1024)
        rtf = conv_elapsed / audio_duration if audio_duration > 0 else 0

        log_lines.append(
            f"  {upload_file.name} → {output_file.name}"
            f"  {input_size_mb:.2f}MB → {output_size_mb:.2f}MB"
            f"  [{conv_elapsed:.1f}s, RTF={rtf:.4f}x]"
        )

        results.append(
            {
                "original": upload_file.name,
                "converted": output_file.name,
                "input_size_mb": round(input_size_mb, 2),
                "output_size_mb": round(output_size_mb, 2),
                "duration_sec": round(audio_duration, 2),
                "rtf": round(rtf, 4),
            }
        )

    return results, log_lines


def _load_model() -> tuple:
    """
    Load Demucs htdemucs_ft model. Runs in ThreadPool while ffmpeg is running.
    Returns (separator, log_lines).
    """
    from demucs.pretrained import get_model

    log_lines: list[str] = []

    # Demucs stores models in ~/.cache/torch/ by default.
    # Symlink ~/.cache to our models volume so downloads persist.
    cache_dir = Path.home() / ".cache"
    models_dir = Path(config.MOUNT_MODELS)

    if not cache_dir.is_symlink():
        if cache_dir.exists():
            shutil.rmtree(cache_dir)
        cache_dir.symlink_to(models_dir, target_is_directory=True)
        print(f"    [cache] symlink: {cache_dir} -> {models_dir}")

    models_dir.mkdir(parents=True, exist_ok=True)

    if models_dir.exists():
        total_size = sum(f.stat().st_size for f in models_dir.rglob("*") if f.is_file())
        cache_mb = total_size / (1024 * 1024)
    else:
        cache_mb = 0.0

    log_lines.append(f"  Demucs htdemucs_ft  [cache: {cache_mb:.2f}MB]")

    model_t0 = time.monotonic()
    separator = get_model("htdemucs_ft")
    model_elapsed = time.monotonic() - model_t0
    log_lines.append(f"  model init: {model_elapsed:.1f}s")

    return separator, log_lines


@images.app_isolate.function(
    image=images.image_isolate,
    gpu=config.GPU_TYPE,
    volumes={
        config.MOUNT_DATA: images.volume_data,
        config.MOUNT_MODELS: images.volume_models,
    },
    timeout=config.TIMEOUT_DENOISE,
    retries=0,
)
def isolate(slug: str) -> list[dict]:
    """
    Single-stage vocal isolation on L4 GPU.

    ffmpeg conversion (CPU) and model loading (GPU) run in parallel via ThreadPoolExecutor.
    Then GPU inference processes each .flac file sequentially.
    """
    t0 = time.monotonic()

    upload_dir = Path(config.MOUNT_DATA) / slug / config.DIR_UPLOAD
    intermediate_dir = Path(config.TMP_PREFIX_ISOLATE) / slug
    output_dir = Path(config.MOUNT_DATA) / slug / config.DIR_OUTPUT
    output_dir.mkdir(parents=True, exist_ok=True)

    if not upload_dir.exists():
        print(f"[ERROR] Upload directory does not exist: {upload_dir}")
        return []

    upload_files = [f for f in upload_dir.iterdir() if f.is_file()]
    print(f"[ffmpeg] {len(upload_files)} file(s) to convert")
    print("[model]  loading...")

    # -----------------------------------------------------------
    # Parallel: ffmpeg (CPU) + model load (GPU)
    # -----------------------------------------------------------
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        ffmpeg_future = executor.submit(_run_ffmpeg, upload_dir, intermediate_dir)
        model_future = executor.submit(_load_model)

        ffmpeg_results, ffmpeg_lines = ffmpeg_future.result()
        separator, model_lines = model_future.result()

    # Print buffered parallel-phase logs
    for line in ffmpeg_lines:
        print(line)
    for line in model_lines:
        print(line)

    if not ffmpeg_results:
        print("[ffmpeg] no audio files found")
        return []

    # -----------------------------------------------------------
    # Serial: GPU inference on each .flac file
    # -----------------------------------------------------------
    import soundfile as sf
    from demucs.apply import apply_model
    from demucs.separate import load_track

    flac_files = sorted(intermediate_dir.glob(f"*{config.FLAC_EXTENSION}"))
    total_audio_sec = 0.0

    print(f"\n[gpu]  {len(flac_files)} file(s) to process")
    results = []

    for flac_file in flac_files:
        output_path = output_dir / f"{flac_file.stem}{config.VOCALS_SUFFIX}"

        # Get duration from the intermediate .flac (48kHz)
        audio_info = sf.info(str(flac_file))
        audio_duration = audio_info.frames / audio_info.samplerate
        total_audio_sec += audio_duration

        file_size = flac_file.stat().st_size / (1024 * 1024)

        proc_t0 = time.monotonic()
        sys.stdout.flush()

        # Load audio — Demucs will resample to separator's native samplerate
        mix = load_track(
            str(flac_file),
            audio_channels=2,
            samplerate=separator.samplerate,
        )

        # Separate — split=True is MANDATORY for htdemucs_ft
        # (training length is ~343980 samples, ~7.8s @ 44.1kHz)
        estimates = apply_model(
            separator,
            mix.unsqueeze(0),
            split=True,
            progress=False,
            device="cuda",
        )

        # Extract vocals (vocals is last source in htdemucs_ft: drums/bass/other/vocals)
        vocals_idx = separator.sources.index("vocals")
        vocals = estimates[0, vocals_idx]  # (channels, time)
        proc_elapsed = time.monotonic() - proc_t0
        rtf = proc_elapsed / audio_duration if audio_duration > 0 else 0

        # Save vocals to Volume
        vocals_np = vocals.cpu().numpy().T  # (channels, time) → (time, channels)
        buffer = io.BytesIO()
        sf.write(
            buffer,
            vocals_np,
            samplerate=separator.samplerate,
            subtype=config.AUDIO_SUBTYPE,
        )
        buffer.seek(0)
        output_path.write_bytes(buffer.getvalue())

        output_size = output_path.stat().st_size / (1024 * 1024)

        print(
            f"  {output_path.name}"
            f"  {file_size:.2f}MB → {output_size:.2f}MB"
            f"  [{proc_elapsed:.1f}s, RTF={rtf:.2f}x]"
            f"  dur={audio_duration:.0f}s"
        )

        results.append(
            {
                "input": flac_file.name,
                "output": output_path.name,
                "input_size_mb": round(file_size, 2),
                "output_size_mb": round(output_size, 2),
                "duration_sec": round(audio_duration, 2),
                "rtf": round(rtf, 3),
            }
        )

    # Clean up intermediate .flac files from container SSD
    shutil.rmtree(Path(config.TMP_PREFIX_ISOLATE) / slug, ignore_errors=True)

    elapsed = time.monotonic() - t0
    total_rtf = elapsed / total_audio_sec if total_audio_sec > 0 else 0

    bar = "─" * 50
    print(f"\n{bar}")
    print(
        f"  done. {len(results)} files,"
        f"  audio={total_audio_sec:.0f}s,"
        f"  wall={elapsed:.1f}s,"
        f"  RTF={total_rtf:.2f}x"
    )
    print(bar)

    images.volume_data.commit()

    return results


@images.app_isolate.local_entrypoint()
def main(slug: str) -> None:
    """CLI entry point: modal run isolate.py --slug <slug>"""
    results = isolate.remote(slug)

    if results:
        print(f"\nPipeline complete. Isolated vocals from {len(results)} files.")
    else:
        print("\nPipeline completed but no files were processed.")


if __name__ == "__main__":
    images.app_isolate.run()
