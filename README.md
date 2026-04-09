# Speech & Vocal Skills

Speech/audio processing skills — runs on **[Modal](https://modal.com)**, powered by **[Speech2SRT](https://speech2srt.com)**.

> Modal provides $30 in free GPU compute monthly — enough to process hundreds of audio files with these skills at zero cost.

## Available Skills

- [x] **`speech-denoise`** — Studio-quality vocal denoising via ClearerVoice-Studio MossFormer2. Upload noisy audio, get clean speech.
- [x] **`speech-isolate`** — Vocal isolation / background music removal via Demucs htdemucs_ft. Extract clean vocals from audio with background music.

## Installation

```bash
# All skills via skills.sh (Claude Code, Pochi, etc.)
npx skills add speech2srt/skills

# Specific skill
npx skills add speech2srt/skills@speech-denoise
npx skills add speech2srt/skills@speech-isolate

# For OpenClaw: install via ClawHub CLI
clawhub install speech-denoise
clawhub install speech-isolate
```

## Development

Pipeline code lives at the repo root and is synced to `skills/` via pre-commit hook:

```
denoise.py          ← speech-denoise entry point
isolate.py          ← speech-isolate entry point
src/                ← config, images (synced to all skills)
skills/
├── speech-denoise/ ← bundled with denoise.py + src/
└── speech-isolate/ ← bundled with isolate.py + src/
```

## Acknowledgments

- [Modal](https://modal.com) — GPU cloud infrastructure
- [ClearerVoice-Studio](https://huggingface.co/samson-castalk/ClearerVoice-Studio) — ClearerVoice-Studio speech enhancement toolkit (MossFormer2 model)
- [Demucs](https://github.com/facebookresearch/demucs) — Hybrid Transformer for music source separation (htdemucs_ft model)
- [skills.sh](https://skills.sh) — open agent skills ecosystem
- [ClawHub](https://clawhub.ai) — skill distribution platform
