"""
Modal image and infrastructure definitions - imported as: import src.images as images
"""

import modal

import src.config as config


# ============================================================
# Volumes
# ============================================================
volume_data = modal.Volume.from_name(config.VOLUME_DATA_NAME, create_if_missing=True)
volume_models = modal.Volume.from_name(
    config.VOLUME_MODELS_NAME, create_if_missing=True
)


# ============================================================
# Images
# ============================================================

# Lightweight CPU image: only ffmpeg, no ML dependencies
image_ingress = modal.Image.debian_slim(
    python_version=config.PYTHON_VERSION
).apt_install("ffmpeg")

# Full GPU image: inherits from image_ingress, adds clearvoice + torch
image_denoise = image_ingress.pip_install(
    [
        "clearvoice",
        "torch>=2.0.1",
        "torchaudio>=2.0.2",
    ]
)


# ============================================================
# App Instance
# ============================================================
app = modal.App(config.APP_NAME)
