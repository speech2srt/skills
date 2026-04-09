"""
Pipeline constants - imported as: import src.config as config
"""

# ============================================================
# Shared Infrastructure
# ============================================================
GPU_TYPE = "L4"
PYTHON_VERSION = "3.11"

# Shared Volume names — both denoise and isolate use the same volumes
# Isolation is provided by slug (different directories under the same volume)
VOLUME_DATA_NAME = "speech2srt-data"
VOLUME_MODELS_NAME = "speech2srt-models"

# Shared Volume mount points
MOUNT_DATA = "/mnt/data"
MOUNT_MODELS = "/mnt/models"

# Pipeline directory names (same for both pipelines)
DIR_UPLOAD = "upload"  # under /mnt/data/<slug>/
DIR_OUTPUT = "output"  # under /mnt/data/<slug>/

# Intermediate files written to container SSD (not volume)
# Separate prefixes so denoise/isolate don't conflict during parallel runs
TMP_PREFIX_DENOISE = "/tmp/speech2srt-denoise"
TMP_PREFIX_ISOLATE = "/tmp/speech2srt-isolate"

# ============================================================
# App Name
# ============================================================
APP_NAME = "speech2srt.com"

# ============================================================
# Output Suffixes
# ============================================================
ENHANCED_SUFFIX = "_enhanced.wav"  # denoise pipeline output
VOCALS_SUFFIX = "_vocals.wav"  # isolate pipeline output

# ============================================================
# Legacy aliases (TMP_PREFIX used by denoise.py)
# ============================================================
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

# ============================================================
# Timeout Config (seconds)
# ============================================================
TIMEOUT_DENOISE = 1800  # Single stage (GPU)
FFMPEG_TIMEOUT = 300  # per-file conversion
FFPROBE_TIMEOUT = 30  # per-file probe
