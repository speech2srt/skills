<div align="center">

![banner](banner.jpg)

# Speech & Vocal Skills

**Your voice recordings, now noise-free.**

Built for ourselves. Open to everyone.

[🇺🇸 English](README.md) | [🇨🇳 简体中文](README_CN.md) | [🇹🇼 繁體中文](README_TW.md)

</div>

---

## 🎤 speech-denoise

Your audio sounds perfect. Except for the background noise.

Air conditioner hum, street traffic, electrical interference, your preamp's mysterious buzz — run the skill, get clean audio back.

Works with: `.m4a` `.mp3` `.mp4` `.wav` `.flac` `.ogg` `.aac` `.mov` `.avi`

```bash
denoise these files: /path/to/file1, /path/to/file2...
```

---

## 🎵 speech-isolate

Pull the vocals out of any song or recording.

Background music drowning out your voice? This gives you a clean vocal track — no music, no noise, ready for transcription.

---

## 🎙️ speech-transcribe

3x Faster than Whisper, Speech-to-text with sentence-level timestamps.

You get two outputs: plain text (`.txt`) for documents and subtitles (`.srt`) you can import directly into any video editor.

---

## 📦 Installation

```bash
npx skills add speech2srt/skills
```

Or tell your agent: `install speech-denoise`, `install speech-isolate`, or `install speech-transcribe`.

---

## 🚀 Performance

**L4 GPU on Modal — real-world benchmarks:**

| Skill | Audio Duration | GPU Time | Wall Time | RTF |
|-------|----------------|----------|-----------|-----|
| speech-denoise | ~17 min (2 files) | 48s | 80s | 0.08x |
| speech-isolate | ~5.8 min (1 file) | 90s | 135s | 0.39x |
| speech-transcribe | ~6 min (1 file, large-v3) | 70s | 75s | 0.19x |

> Modal [L4 GPU](https://modal.com/pricing) is $0.80/hr. They give **$30 free credits monthly** — 37 hours of L4 time. At RTF 0.4x, that's **93+ hours of audio for free**. Enough for a solo creator or a small studio.

---

## 🙏 Acknowledgments

- [Modal](https://modal.com) — GPU infrastructure
- [ClearerVoice-Studio](https://huggingface.co/samson-castalk/ClearerVoice-Studio) — MossFormer2
- [Demucs](https://github.com/facebookresearch/demucs) — vocal separation
- [Whisper](https://github.com/openai/whisper) — speech recognition
- [faster-whisper](https://github.com/guillaumekln/faster-whisper) — fast inference
- [skills.sh](https://skills.sh) — skills ecosystem
- [ClawHub](https://clawhub.ai) — distribution

---

## 🔧 Development

See [DEVELOPMENT.md](DEVELOPMENT.md) for details.
