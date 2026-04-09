# Denoise Service

Single-stage speech enhancement — extract audio from any format and enhance with ClearVoice MossFormer2 on L4 GPU.

## Quick Start

```bash
# Create volumes (one-time)
modal volume create speech2srt-denoise-data
modal volume create speech2srt-denoise-models

# Run locally
    modal run denoise.py --slug <slug>
```

## How It Works

1. Upload files to `upload/` in the volume
2. Run the pipeline — audio is extracted and enhanced in a single GPU stage
3. Download results from `output/`

## File Transfer

```bash
# Upload files to upload/
modal volume put speech2srt-denoise-data ./your-audio.mp4 /<slug>/upload/

# Download results from output/
modal volume get speech2srt-denoise-data /<slug>/output/ ./path/to/results_dir
```

## Deploy

```bash
    modal deploy denoise.py
```

## Acknowledgments

- [ClearVoice](https://huggingface.co/spaces/alibabasglab/ClearVoice) — MossFormer2 speech enhancement
- [Modal](https://modal.com) — GPU cloud infrastructure
