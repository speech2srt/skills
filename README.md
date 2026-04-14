<div align="center">

![banner](banner.jpg)

# Speech & Vocal Skills

**Your voice recordings, now noise-free.**

Recorded in a noisy apartment? Your preamp humming? Plane flying overhead?
This skill fixes it. Denoise audio in seconds - runs on Modal L4 GPU and FREE.

Built for ourselves. Open to everyone.

[🇺🇸 English](README.md) | [🇨🇳 简体中文](README_CN.md) | [🇹🇼 繁體中文](README_TW.md)

</div>

---

## 🎤 speech-denoise

Your audio sounds perfect. Except for the background noise.

Whether it's an air conditioner hum, street traffic, electrical interference, or that mysterious buzz your preamp won't stop making - run the skill, get clean audio back.

Works with any format: `.m4a`, `.mp3`, `.mp4`, `.wav`, `.flac`, `.ogg`, `.aac`, `.mov`, `.avi`.

Just tell your AI agent:
```bash
denoise these files: /path/to/file1, /path/to/file2...
```

No audio editing skills required.

---

## 📦 Installation

```bash
npx skills add speech2srt/skills
```

For OpenClaw, just tell your agent: `install speech-denoise skill`, `install speech-isolate skill`, or `install speech-transcribe skill`.

---

## ✨ One more thing...

### 🎵 speech-isolate

**🎵 speech-isolate** - Pull the vocals out of any song or recording.

Background music drowning out your recording? This pulls the voice out and cleans it up in one pass. The result is a pure vocal track — no music, no noise, ready for transcription or any other use.

> **Tip:** Background music confuses speech recognition — remove it first, get cleaner transcripts.

### 🎙️ speech-transcribe

**🎙️ speech-transcribe** — Speech-to-text transcription with sentence-level timestamps.

Powered by Whisper (large-v3 model) with VAD (Voice Activity Detection) for accurate silence suppression and timestamp alignment. Outputs both plain text (`.txt`) and subtitles (`.srt`) so you can subtitle your videos or import into any editor.

> **Best result:** Run `speech-isolate` first, then `speech-transcribe` — clean vocals give you cleaner transcripts.

---

## 🚀 Performance

**L4 GPU on Modal - real-world benchmarks:**

| Skill | Audio Duration | GPU Time | Wall Time | RTF |
|-------|----------------|----------|-----------|-----|
| speech-denoise | ~17 min (2 files) | 48s | 80s | 0.08x |
| speech-isolate | ~5.8 min (1 file) | 90s | 135s | 0.39x |
| speech-transcribe | ~6 min (1 file, large-v3) | 70s | 75s | 0.19x |

> **Note:** `speech-isolate` runs a two-stage pipeline: Demucs (vocal separation) + ClearerVoice MossFormer2 (speech enhancement). GPU time is the combined inference time of both stages. The higher RTF reflects the sequential nature of running two models per file.

> **Note:** `speech-transcribe` uses Whisper large-v3 with VAD enabled on L4 GPU. RTF measured with int8_float16 compute type. Model options: `tiny` (RTF ~0.03x), `base` (RTF ~0.06x), `small` (RTF ~0.09x), `medium` (RTF ~0.13x), `large-v3` (RTF ~0.19x).

Modal [L4 GPU](https://modal.com/pricing) runs $0.80/hr, but they give **$30 free credits monthly** - that's 37 hours of L4 GPU time. At RTF 0.4x, **you can process 93+ hours of audio for ZERO dollars**. More than enough for a solo creator or a small studio.

---

## 🙏 Acknowledgments

- [Modal](https://modal.com) - GPU cloud infrastructure
- [ClearerVoice-Studio](https://huggingface.co/samson-castalk/ClearerVoice-Studio) - speech enhancement toolkit (MossFormer2 model)
- [Demucs](https://github.com/facebookresearch/demucs) - music source separation (htdemucs_ft model)
- [Whisper](https://github.com/openai/whisper) - speech recognition (large-v3 model)
- [faster-whisper](https://github.com/guillaumekln/faster-whisper) - fast Whisper implementation
- [skills.sh](https://skills.sh) - open agent skills ecosystem
- [ClawHub](https://clawhub.ai) - OpenClaw skills distribution platform

---

## 🔧 Development

See [DEVELOPMENT.md](DEVELOPMENT.md) for details.
