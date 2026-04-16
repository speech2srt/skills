# AGENTS.md — Skills Collection

## Project Overview

Independent skill packages, each self-contained with its own pipeline code and SKILL.md.

## Skills

| Skill | Description |
|-------|-------------|
| `speech-denoise` | Vocal denoising via ClearerVoice-Studio MossFormer2 on Modal L4 GPU |
| `speech-isolate` | Vocal isolation / background music removal via Demucs on Modal L4 GPU |
| `speech-transcribe` | Speech-to-text via faster-whisper on Modal L4 GPU |
| `ocr2markdown` | PDF/document OCR and parsing via MinerU on Modal L4 GPU |

## Architecture

Each skill lives in `skills/<name>/` with its own:

- `SKILL.md` — workflow documentation
- `<name>.py` — Modal entry point
- `src/` — pipeline code (config, images, helpers)
- `references/` — additional docs (optional)

**No shared canonical source.** Each skill is independently runnable after `npx skills add`.

## Shared Infrastructure

All skills use the same Modal infrastructure:

- **App name**: `speech2srt.com`
- **Volumes**: `speech2srt-data`, `speech2srt-models`
- **GPU**: L4

Volume layout per task (`<slug>/upload/` → `<slug>/output/`):

```
upload/          # input files (audio, video, PDF, etc.)
output/          # processed results
```
