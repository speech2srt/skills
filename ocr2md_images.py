import os
from pathlib import Path
import modal
import ocr2md_config as config


volume_data = modal.Volume.from_name(config.VOLUME_DATA_NAME, create_if_missing=True)
volume_models = modal.Volume.from_name(
    config.VOLUME_MODELS_NAME, create_if_missing=True
)


_image = (
    modal.Image.from_registry("vllm/vllm-openai:v0.11.2", add_python="3.12")
    .entrypoint([])
    .run_commands(
        "python3 -m pip install --no-cache-dir 'mineru[core]>=3.0.0' opencv-python-headless --break-system-packages -q"
    )
    .env(
        {
            "MINERU_MODEL_SOURCE": "huggingface",
            "HF_HUB_DISABLE_PROGRESS": "1",
            "TQDM_DISABLE": "1",
        }
    )
    .add_local_file(
        os.path.dirname(__file__) + "/ocr2md_config.py",
        remote_path="/root/src/ocr2md_config.py",
    )
    .add_local_file(
        os.path.dirname(__file__) + "/ocr2md_images.py",
        remote_path="/root/src/ocr2md_images.py",
    )
)


image_ocr2markdown = _image


app = modal.App(config.APP_NAME)
