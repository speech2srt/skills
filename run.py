"""
Modal service: Two-stage speech enhancement pipeline

Stage 1 - Ingress (CPU): Converts any audio/video file in upload/ to 48kHz .flac in input/
Stage 2 - Denoise (L4 GPU): Enhances .flac files from input/ to output/

Usage:
    modal run run.py --path <path>
"""

from src import config, images, ingress, denoise


@images.app.local_entrypoint()
def main(path: str) -> None:
    """CLI entry point: modal run run.py --path <path>"""
    print(f"Starting pipeline for path: {path}")
    print(f"Upload directory: {config.MOUNT_DATA}/{path}/{config.DIR_UPLOAD}")
    print(f"Input directory:  {config.MOUNT_DATA}/{path}/{config.DIR_INPUT}")
    print(f"Output directory: {config.MOUNT_DATA}/{path}/{config.DIR_OUTPUT}")
    print()

    # Stage 1: Ingress (CPU) - converts uploads to standardized flac
    results = ingress.ingress.remote(path)

    if not results:
        print("\nIngress completed but no audio files were converted.")
        return

    print(f"\nIngress complete. Converted {len(results)} files.")
    print("Starting denoise stage on L4 GPU...")

    # Stage 2: Denoise (L4 GPU) - enhances flac files
    # Call directly instead of spawn to ensure it runs after ingress completes
    denoise_results = denoise.denoise.remote(path)

    if denoise_results:
        print(f"\nPipeline complete. Enhanced {len(denoise_results)} files.")
    else:
        print("\nDenoise stage completed but no files were enhanced.")


if __name__ == "__main__":
    images.app.run()
