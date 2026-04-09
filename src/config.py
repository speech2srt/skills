"""
Pipeline constants - imported as: import src.config as config
"""

# ============================================================
# App & Infrastructure Config (shared)
# ============================================================
GPU_TYPE = "L4"
PYTHON_VERSION = "3.11"

# ============================================================
# Denoise Pipeline Config
# ============================================================
APP_NAME_DENOISE = "denoise-by-speech2srt.com"

# Volume names
VOLUME_DATA_NAME_DENOISE = "speech2srt-denoise-data"
VOLUME_MODELS_NAME_DENOISE = "speech2srt-denoise-models"

# Volume mount points
MOUNT_DATA_DENOISE = "/mnt/data"
MOUNT_MODELS_DENOISE = "/mnt/models"

# Pipeline directory names
DIR_UPLOAD = "upload"  # under /mnt/data/<path>/
DIR_OUTPUT = "output"  # under /mnt/data/<path>/

# Intermediate files written to container SSD (not volume)
TMP_PREFIX_DENOISE = "/tmp/speech2srt-denoise"

# ============================================================
# Isolate Pipeline Config
# ============================================================
APP_NAME_ISOLATE = "isolate-by-speech2srt.com"

# Volume names
VOLUME_DATA_NAME_ISOLATE = "speech2srt-isolate-data"
VOLUME_MODELS_NAME_ISOLATE = "speech2srt-isolate-models"

# Volume mount points
MOUNT_DATA_ISOLATE = "/mnt/isolate-data"
MOUNT_MODELS_ISOLATE = "/mnt/isolate-models"

# Intermediate files written to container SSD (not volume)
TMP_PREFIX_ISOLATE = "/tmp/speech2srt-isolate"

# Output suffix for isolated vocals
VOCALS_SUFFIX = "_vocals.wav"

# ============================================================
# Legacy aliases (temporary - denoise.py uses these directly)
# ============================================================
APP_NAME = APP_NAME_DENOISE
VOLUME_DATA_NAME = VOLUME_DATA_NAME_DENOISE
VOLUME_MODELS_NAME = VOLUME_MODELS_NAME_DENOISE
MOUNT_DATA = MOUNT_DATA_DENOISE
MOUNT_MODELS = MOUNT_MODELS_DENOISE
TMP_PREFIX = TMP_PREFIX_DENOISE

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
TIMEOUT_DENOISE = 1800  # Single stage (GPU)
FFMPEG_TIMEOUT = 300  # per-file conversion
FFPROBE_TIMEOUT = 30  # per-file probe
