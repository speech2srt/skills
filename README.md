<div align="center">

![banner](banner.jpg)

# Speech & Vocal Skills

Built for ourselves. Open to everyone.

Speech/audio processing skills — runs on **[Modal](https://modal.com)**, created by **[Speech2SRT](https://speech2srt.com)**.

[English](README.md) | [简体中文](README_CN.md) | [繁體中文](README_TW.md)

</div>

---

> Many thanks to **[Modal](https://modal.com)**, they provides $30 in free GPU compute monthly — enough to process hundreds of audio files with these skills at zero cost.

## Available Skills

### 1. speech-denoise

Studio-quality vocal denoising via ClearerVoice-Studio `MossFormer2`. Upload noisy audio, get clean speech.

### 2. speech-isolate

Vocal isolation / background music removal via Demucs `htdemucs_ft`. Extract clean vocals from audio with background music.

## Performance

**L4 GPU on Modal — real-world benchmarks:**

| Skill | Audio Duration | GPU Time | Wall Time | RTF |
|-------|----------------|----------|-----------|-----|
| speech-denoise | ~17 min (2 files) | 48s | 80s | 0.08x |
| speech-isolate | ~6 min (1 file) | 30s | 36s | 0.09x |

## Installation

```bash
# For Claude Code, Antigravity, etc.
npx skills add speech2srt/skills

# For OpenClaw
clawhub install speech-denoise
clawhub install speech-isolate
```

> If you are using [OpenClaw](https://openclaw.ai), just ask you pal to `install speech-denoise skill` or `install speech-isolate skill`.

## Development

See [DEVELOPMENT.md](DEVELOPMENT.md) for details.

## Acknowledgments

- [Modal](https://modal.com) — GPU cloud infrastructure
- [ClearerVoice-Studio](https://huggingface.co/samson-castalk/ClearerVoice-Studio) — ClearerVoice-Studio speech enhancement toolkit (MossFormer2 model)
- [Demucs](https://github.com/facebookresearch/demucs) — Hybrid Transformer for music source separation (htdemucs_ft model)
- [skills.sh](https://skills.sh) — open agent skills ecosystem
- [ClawHub](https://clawhub.ai) — OpenClaw skills distribution platform
