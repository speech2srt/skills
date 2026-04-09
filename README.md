# Speech & Vocal Skills

Speech/audio processing skills powered by **[Modal](https://modal.com)** — each skill runs GPU workloads on Modal's L4 instances at no cost, thanks to Modal's **$30/month free credit** for new users.

> Modal provides $30 in free GPU compute monthly — enough to process hundreds of audio files with these skills at zero cost.

## Available Skills

| Skill | Description |
|-------|-------------|
| `speech-denoise` | Vocal denoising via ClearVoice MossFormer2 on Modal L4 GPU. Takes audio/video files, returns noise-reduced audio. |

## Installation

### Via `npx skills` (skills.sh ecosystem)

Requires: [skills.sh compatible client](https://skills.sh) (Claude Code, OpenClaw, Pochi, etc.)

**Install all skills:**
```bash
npx skills add speech2srt/skills
```

**Install specific skill:**
```bash
npx skills add speech2srt/skills@speech-denoise
# or
npx skills add speech2srt/skills --skill speech-denoise
```

**List available skills without installing:**
```bash
npx skills add speech2srt/skills --list
```

**Local development:**
```bash
npx skills add ./skills --list
npx skills add ./skills --skill speech-denoise
```

### Via ClawHub

Requires: [ClawHub CLI](https://clawhub.ai) — `npx clawhub@latest` or install via Bun/m npm

```bash
# Install from ClawHub
clawhub install speech-denoise
# or via full path
clawhub install speech2srt/speech-denoise
```

See [clawhub.ai/speech2srt/speech-denoise](https://clawhub.ai/speech2srt/speech-denoise) for details, version history, and security scan.

## Skill: speech-denoise

**What it does:** Uploads local audio/video files to Modal volume, runs ClearVoice MossFormer2 GPU inference, downloads enhanced results.

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

- [ClearerVoice-Studio](https://huggingface.co/samson-castalk/ClearerVoice-Studio) — ClearVoice speech enhancement model
- [Modal](https://modal.com) — GPU cloud infrastructure
- [skills.sh](https://skills.sh) — open agent skills ecosystem
- [ClawHub](https://clawhub.ai) — skill distribution platform
