# Speech & Vocal Skills

Speech/audio processing skills — runs on **[Modal](https://modal.com)**, powered by **[Speech2SRT](https://speech2srt.com)**.

> Modal provides $30 in free GPU compute monthly — enough to process hundreds of audio files with these skills at zero cost.

## Available Skills

### 1. speech-denoise

Studio-quality vocal denoising via ClearerVoice-Studio MossFormer2. Upload noisy audio, get clean speech.

### 2. speech-isolate

Vocal isolation / background music removal via Demucs htdemucs_ft. Extract clean vocals from audio with background music.

## Installation

```bash
# For Claude Code, Antigravity, etc.
npx skills add speech2srt/skills

# For OpenClaw
clawhub install speech-denoise
clawhub install speech-isolate
```

## Development

Pipeline code lives at the repo root and is synced to `skills/` via pre-commit hook.

`pre-commit.sh` located at project root, this hook runs automatically on `git commit` (when properly symlinked):

**What it does:**
1. **Syntax check** — validates Python entry points (`denoise.py`, `isolate.py`) with `py_compile`
2. **Bundle sync** — copies entry points and `src/` directory into each skill bundle
3. **Cleanup** — removes `__pycache__` and `.pyc` files across the repo

**Setup (already done — for reference):**
```bash
# Create symlink to enable the hook
ln -sf ../../pre-commit.sh .git/hooks/pre-commit
```

**File structure:**
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
- [ClawHub](https://clawhub.ai) — OpenClaw skills distribution platform
