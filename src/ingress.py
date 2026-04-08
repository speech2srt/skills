"""Stage 1: Ingress (CPU) - Audio extraction & normalization."""

import subprocess
from pathlib import Path

import src.config as config
import src.images as images


@images.app.function(
    image=images.image_ingress,
    volumes={
        config.MOUNT_DATA: images.volume_data,
    },
    timeout=config.TIMEOUT_INGRESS,
)
def ingress(path: str) -> list[dict]:
    """Convert all audio/video files in /mnt/data/<path>/upload to 48kHz .flac in /mnt/data/<path>/input."""
    import json

    upload_dir = Path(config.MOUNT_DATA) / path / config.DIR_UPLOAD
    input_dir = Path(config.MOUNT_DATA) / path / config.DIR_INPUT
    input_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n[INGRESS] Scanning: {upload_dir}")
    if not upload_dir.exists():
        print(f"    Upload directory does not exist: {upload_dir}")
        return []

    upload_files = [f for f in upload_dir.iterdir() if f.is_file()]
    print(f"    Found {len(upload_files)} files")

    results = []
    for upload_file in upload_files:
        probe_cmd = [
            "ffprobe",
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_streams",
            str(upload_file),
        ]
        try:
            probe_result = subprocess.run(
                probe_cmd,
                capture_output=True,
                text=True,
                timeout=config.FFPROBE_TIMEOUT,
            )
            streams = json.loads(probe_result.stdout).get("streams", [])
            has_audio = any(s.get("codec_type") == "audio" for s in streams)
        except Exception as e:
            print(f"    [WARN] ffprobe failed for {upload_file.name}: {e}")
            has_audio = False

        if not has_audio:
            print(f"    [SKIP] {upload_file.name} - no audio stream")
            continue

        output_file = input_dir / f"{upload_file.stem}{config.FLAC_EXTENSION}"

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

        print(f"    [CONVERT] {upload_file.name} -> {output_file.name}")
        try:
            subprocess.run(
                ffmpeg_cmd,
                capture_output=True,
                text=True,
                timeout=config.FFMPEG_TIMEOUT,
                check=True,
            )
            input_size_mb = upload_file.stat().st_size / (1024 * 1024)
            output_size_mb = output_file.stat().st_size / (1024 * 1024)
            print(f"            {input_size_mb:.2f} MB -> {output_size_mb:.2f} MB")

            results.append(
                {
                    "original": upload_file.name,
                    "converted": output_file.name,
                    "input_size_mb": round(input_size_mb, 2),
                    "output_size_mb": round(output_size_mb, 2),
                }
            )
        except subprocess.CalledProcessError as e:
            print(f"    [ERROR] ffmpeg failed for {upload_file.name}: {e.stderr}")

    print(f"\n[INGRESS] Done. Converted {len(results)} files")
    images.volume_data.commit()

    print("[INGRESS] Spawning denoise stage...")

    # Import here to avoid circular import at module level
    from src import denoise as denoise_module

    denoise_module.denoise.spawn(path)

    return results
