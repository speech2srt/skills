<div align="center">

![banner](banner.jpg)

# Speech & Vocal Skills

**你的录音，从此没有噪音。**

Built for ourselves. Open to everyone.

[🇺🇸 English](README.md) | [🇨🇳 简体中文](README_CN.md) | [🇹🇼 繁體中文](README_TW.md)

</div>

---

## 🎤 speech-denoise

你的录音听起来不错，除了背景噪音。

空调嗡嗡声、街上车流、电流干扰、功放的莫名杂音——运行这个 Skill，还你干净的音频。

支持格式：`.m4a` `.mp3` `.mp4` `.wav` `.flac` `.ogg` `.aac` `.mov` `.avi`

```bash
denoise these files: /path/to/file1, /path/to/file2...
```

---

## 🎵 speech-isolate

提取录音中的人声。

录音里有背景音乐？这个人声提取工具给你一条干净的人声音轨——没有音乐、没有噪音，可以直接用于转写。

---

## 🎙️ speech-transcribe

比 Whisper 快 3 倍，语音转文字，带句级时间戳。

输出两种格式：纯文本（`.txt`）用于文档，字幕文件（`.srt`）可直接导入任何视频编辑器。

---

## 📦 Installation

```bash
npx skills add speech2srt/skills
```

或告诉你的 agent：`install speech-denoise`、`install speech-isolate` 或 `install speech-transcribe`。

---

## 🚀 Performance

**L4 GPU on Modal — 实测数据：**

| Skill | 音频时长 | GPU 时间 | 总耗时 | RTF |
|-------|----------|---------|--------|-----|
| speech-denoise | ~17 分钟（2 个文件） | 48s | 80s | 0.08x |
| speech-isolate | ~5.8 分钟（1 个文件） | 90s | 135s | 0.39x |
| speech-transcribe | ~6 分钟（1 个文件，large-v3） | 59s | 73s | 0.21x |

**speech-transcribe 模型选项**（~6 分钟音频实测）：

| 模型 | 初始化 | GPU 推理 | 总耗时 | RTF |
|------|--------|----------|--------|-----|
| tiny | 1.2s | 15.9s | 22s | 0.06x |
| base | 4.1s | 18.0s | 29s | 0.08x |
| small | 5.9s | 24.0s | 36s | 0.10x |
| medium | 10.3s | 36.3s | 51s | 0.15x |
| large-v3 | 8.3s | 58.8s | 73s | 0.21x |

> Modal [L4 GPU](https://modal.com/pricing) 每小时 $0.80，但他们每月赠送 **$30 额度**——相当于 37 小时 L4 GPU 时间。按 RTF 0.4x 算，**你可以处理超过 93 小时的音频，分文不花**。个人创作者或小型工作室，绰绰有余。

---

## 🙏 Acknowledgments

- [Modal](https://modal.com) — GPU 基础设施
- [ClearerVoice-Studio](https://huggingface.co/samson-castalk/ClearerVoice-Studio) — MossFormer2
- [Demucs](https://github.com/facebookresearch/demucs) — 人声分离
- [Whisper](https://github.com/openai/whisper) — 语音识别
- [faster-whisper](https://github.com/guillaumekln/faster-whisper) — 快速推理
- [skills.sh](https://skills.sh) — Skills 生态
- [ClawHub](https://clawhub.ai) — 分发平台

---

## 🔧 Development

See [DEVELOPMENT.md](DEVELOPMENT.md) for details.
