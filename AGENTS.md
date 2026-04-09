# AGENTS.md — Speech Processing Skills

## Project Overview

Speech/audio processing skills collection. Root-level code (`denoise.py`, `src/`) is the canonical source; `skills/` contains distributable skill bundles synced via pre-commit hook.

## Skills

| Skill | Description |
|-------|-------------|
| `speech-denoise` | Vocal denoising via ClearerVoice-Studio MossFormer2 on Modal L4 GPU |

## Canonical Source vs. Skill Bundles

```
denoise.py          # Canonical pipeline entry point
src/                # Canonical config, images
skills/             # Skill bundles (synced from root, DO NOT edit directly)
```

Pre-commit hook (`git/hooks/pre-commit`) syncs `denoise.py` and `src/` into `skills/speech-denoise/` before every commit.

## Pipeline Architecture

## Pipeline Flow

```
/mnt/data/<slug>/upload/*.m4a
    └── [denoise - L4 GPU, ThreadPoolExecutor]
            ├── Thread-1: ffmpeg CPU conversion → /tmp/speech2srt-denoise/<slug>/*.flac
            └── Thread-2: ClearerVoice-Studio model loading (GPU)
            → GPU inference → /mnt/data/<slug>/output/*_enhanced.wav
```

## Parallelization

`ThreadPoolExecutor(max_workers=2)` runs ffmpeg (CPU) and model loading (GPU) concurrently:

- **Cold cache**: model init (36s) dominates, ffmpeg (~5s) completes during model load → wall time ≈ model init
- **Warm cache**: model init (~1s), ffmpeg (~5s) → wall time ≈ max(ffmpeg, model init) ≈ 5s

## Timing Instrumentation

Each stage reports wall-clock elapsed time and RTF (Real-Time Factor = processing_time / audio_duration):

- Per-file ffmpeg RTF
- Per-file GPU inference RTF
- Aggregate stage RTF

## Modal App

- App name: `denoise-by-speech2srt.com`
- Volumes: `speech2srt-denoise-data`, `speech2srt-denoise-models`

## Running

```bash
modal run denoise.py --slug <slug>
```

## Key Conventions

- All constants defined in `src/config.py` — imported as `from src import config`
- Images defined in `src/images.py` — imported as `from src import images`
- `src/` is copied into `image_denoise` via `add_local_dir` so `import src` works in the container
- Single `image_denoise`: debian-slim + ffmpeg + clearvoice + torch + torchaudio
- `image_denoise` image has `TQDM_DISABLE=1` and `HF_HUB_DISABLE_PROGRESS=1` env vars set
- Function retries: disabled (`retries=0`)

## Volume Mounts

| Mount | Volume | Purpose |
|-------|--------|---------|
| `/mnt/data` | speech2srt-denoise-data | upload/, output/ files |
| `/mnt/models` | speech2srt-denoise-models | ClearerVoice-Studio checkpoints |
| `/tmp/speech2srt-denoise/<slug>` | (container SSD) | intermediate .flac files |
