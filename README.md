# Speech & Vocal Skills

Speech/audio processing skills — runs on **[Modal](https://modal.com)**, powered by **[Speech2SRT](https://speech2srt.com)**.

> Modal provides $30 in free GPU compute monthly — enough to process hundreds of audio files with these skills at zero cost.

## Available Skills

- [x] **`speech-denoise`** — Studio-quality vocal denoising via ClearerVoice-Studio MossFormer2. Upload noisy audio, get clean speech.
- [ ] **`speech-remove-bgm`** — Remove background music from voice recordings while preserving speech clarity.

## Installation

```bash
# All skills via skills.sh (Claude Code, Pochi, etc.)
npx skills add speech2srt/skills

# Specific skill
npx skills add speech2srt/skills@speech-denoise

# List all available skills
npx skills add speech2srt/skills --list

# For OpenClaw: install via ClawHub CLI instead
#   npx clawhub@latest          # one-time install ClawHub CLI
#   clawhub install speech-denoise
# See clawhub.ai/speech2srt/speech-denoise for details

## Skill: speech-denoise

**What it does:** Uploads local audio/video files to Modal volume, runs ClearerVoice-Studio MossFormer2 GPU inference, downloads enhanced results.

**Triggers:** "denoise", "去噪", "enhance audio", "remove noise", "clean up audio", "run the denoise pipeline"

**Pipeline:** Single-stage — ffmpeg audio extraction + MossFormer2 speech enhancement in one Modal container on L4 GPU.

See `skills/speech-denoise/SKILL.md` for full workflow.

## Development

Pipeline code lives at the repo root and is synced to `skills/speech-denoise/` via pre-commit hook:

```
denoise.py          ← pipeline entry point
src/                ← config, images (synced to skill)
skills/             ← skill bundles (distributed to agents)
```

## Acknowledgments

- [Modal](https://modal.com) — GPU cloud infrastructure
- [ClearerVoice-Studio](https://huggingface.co/samson-castalk/ClearerVoice-Studio) — ClearerVoice-Studio speech enhancement toolkit (MossFormer2 model)
- [skills.sh](https://skills.sh) — open agent skills ecosystem
- [ClawHub](https://clawhub.ai) — skill distribution platform
