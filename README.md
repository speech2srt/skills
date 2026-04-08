# Denoise Service

Two-stage speech enhancement — extract audio from any format, then enhance with ClearVoice on L4 GPU.

## Quick Start

```bash
# Create volumes (one-time)
modal volume create speech2srt-denoise-data
modal volume create speech2srt-denoise-models

# Run locally
modal run run.py --path <path>
```

## How It Works

1. Upload files to `upload/` in the volume
2. Run the pipeline — audio is extracted to `input/*.flac`, then enhanced to `output/*_enhanced.wav`
3. Download results from `output/`

## File Transfer

```bash
# Upload files to upload/
modal volume put speech2srt-denoise-data ./your-audio.mp4 /<path>/upload/

# Download results from output/
modal volume get speech2srt-denoise-data /<path>/output/ ./path/to/results_dir
```

## Deploy

```bash
modal deploy run.py
```
