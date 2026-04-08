# AGENTS.md — Denoise Service

## Project Overview

Two-stage Modal speech enhancement pipeline using ClearVoice MossFormer2_SE_48K.

## Architecture

```
run.py              # Entry point (local CLI)
src/
  config.py         # All constants
  images.py         # Modal images & app instance
  ingress.py        # Stage 1: CPU audio extraction (ffmpeg)
  denoise.py        # Stage 2: GPU speech enhancement (ClearVoice)
```

## Pipeline Flow

```
/mnt/data/<path>/upload/   → [ingress - CPU]   → /mnt/data/<path>/input/
/mnt/data/<path>/input/*.flac            → [denoise - L4 GPU] → /mnt/data/<path>/output/*_enhanced.wav
```

## Modal App

- App name: `denoise-by-speech2srt.com`
- Volumes: `speech2srt-denoise-data`, `speech2srt-denoise-models`

## Running

```bash
modal run run.py --path <path>
```

## Key Conventions

- All constants defined in `src/config.py` — imported as `from src import config`
- Images defined in `src/images.py` — imported as `from src import images`
- Stage functions use explicit imports from `src.config` and `src.images`
- `ingress` stage spawns `denoise` via `denoise.spawn(path)` at end of execution
- Two separate images: `image_ingress` (CPU + ffmpeg), `image_denoise` (GPU + clearvoice + torch)

## Dependencies

- `image_ingress`: debian-slim + ffmpeg
- `image_denoise`: inherits image_ingress + pip install clearvoice, torch, torchaudio

## Volume Mounts

| Mount | Volume | Purpose |
|-------|--------|---------|
| `/mnt/data` | speech2srt-denoise-data | upload/, input/, output/ files |
| `/mnt/models` | speech2srt-denoise-models | ClearVoice checkpoints |
