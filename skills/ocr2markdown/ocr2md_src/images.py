"""
Modal image and infrastructure for OCR2Markdown pipeline.
"""

from pathlib import Path
import modal
import config


# Volume mounts
volume_data = modal.Volume.from_name(config.VOLUME_DATA_NAME, create_if_missing=True)
volume_models = modal.Volume.from_name(
    config.VOLUME_MODELS_NAME, create_if_missing=True
)


# Build image: vllm/vllm-openai + mineru[all]
# This gives us vLLM + PyTorch + mineru in one container
_src_dir = str(Path(__file__).parent)
_image = (
    modal.Image.from_registry("vllm/vllm-openai:v0.11.2")
    .pip_install("mineru[all]")
    .pip_install("opencv-python-headless")
    .run_commands(
        "pip uninstall -y opencv-python && pip install opencv-python-headless"
    )
    .env(
        {
            "MINERU_MODEL_SOURCE": "local",
            "HF_HUB_DISABLE_PROGRESS": "1",
            "TQDM_DISABLE": "1",
        }
    )
    .add_local_dir(_src_dir, remote_path="/root/src", copy=True)
)

# Function decorator uses this image
image_ocr2markdown = _image


# App instance
app = modal.App(config.APP_NAME)
