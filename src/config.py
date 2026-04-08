"""
Pipeline constants - imported as: import src.config as config
"""

# ============================================================
# App & Infrastructure Config
# ============================================================
APP_NAME = "denoise-by-speech2srt.com"
GPU_TYPE = "L4"
PYTHON_VERSION = "3.11"

# Volume names
VOLUME_DATA_NAME = "speech2srt-denoise-data"
VOLUME_MODELS_NAME = "speech2srt-denoise-models"

# Volume mount points
MOUNT_DATA = "/mnt/data"
MOUNT_MODELS = "/mnt/models"

# Pipeline directory names (under /mnt/data/<path>/)
DIR_UPLOAD = "upload"
DIR_INPUT = "input"
DIR_OUTPUT = "output"

# ============================================================
# Audio Processing Config
# ============================================================
AUDIO_SAMPLE_RATE = 48000  # Hz
AUDIO_CHANNELS = 1  # mono
AUDIO_FORMAT = "WAV"
AUDIO_SUBTYPE = "PCM_24"
AUDIO_STEREO_NDIM = 2  # shape dimension that indicates (channels, samples) layout

# ============================================================
# File Extension Config
# ============================================================
FLAC_EXTENSION = ".flac"
ENHANCED_SUFFIX = "_enhanced.wav"

# ============================================================
# Timeout Config (seconds)
# ============================================================
TIMEOUT_INGRESS = 600  # Stage 1 (CPU)
TIMEOUT_DENOISE = 1800  # Stage 2 (GPU)
FFMPEG_TIMEOUT = 300  # per-file conversion
FFPROBE_TIMEOUT = 30  # per-file probe

# ============================================================
# Debug / Logging Config
# ============================================================
DEBUG_LIST_LIMIT = 20  # max files to print in directory listing
