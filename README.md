# Denoise Service

Single-stage speech enhancement — extract audio from any format and enhance with ClearVoice MossFormer2 on L4 GPU.

## Quick Start

```bash
# Create volumes (one-time)
modal volume create speech2srt-denoise-data
modal volume create speech2srt-denoise-models

# Run locally
    modal run denoise.py --path <path>
```

## How It Works

1. Upload files to `upload/` in the volume
2. Run the pipeline — audio is extracted and enhanced in a single GPU stage
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
    modal deploy denoise.py
```
