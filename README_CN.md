<div align="center">

![banner](banner.jpg)

# Speech & Vocal Skills

**你的录音，从此没有噪音。**

住在嘈杂的公寓？功放有嗡嗡声？头顶有飞机飞过？
这个 Skill 来解决。几秒钟完成去噪——运行在 Modal L4 GPU 上，而且免费。

Built for ourselves. Open to everyone.

[🇺🇸 English](README.md) | [🇨🇳 简体中文](README_CN.md) | [🇹🇼 繁體中文](README_TW.md)

</div>

---

## 🎤 speech-denoise

你的录音听起来不错，除了背景噪音。

不管是空调的嗡嗡声、街上的车流、电流干扰，还是你的功放怎么也去不掉的莫名杂音——运行这个 Skill，还你干净的音频。

支持所有常见格式：`.m4a`、`.mp3`、`.mp4`、`.wav`、`.flac`、`.ogg`、`.aac`、`.mov`、`.avi`。

告诉你的 AI agent：
```bash
denoise these files: /path/to/file1, /path/to/file2...
```

不需要任何音频编辑技能。

---

## 📦 Installation

```bash
npx skills add speech2srt/skills
```

使用 OpenClaw？直接告诉你的 agent：`install speech-denoise skill` 或 `install speech-isolate skill`。

---

## ✨ One more thing...

### 🎵 speech-isolate

**🎵 speech-isolate** — 提取录音中的人声并降噪。

录音里有背景音乐？这个人声提取工具可以帮你把声音分离出来并完成降噪处理。出来的就是干净的人声音轨——没有音乐、没有噪音，可以直接用于转写或其他用途。

> **Tip:** 做 ASR 之前先用这个。背景音乐会干扰语音识别模型——先去音乐，再做识别，字幕更干净。

---

## 🚀 Performance

**L4 GPU on Modal — 实测数据：**

| Skill | 音频时长 | GPU 时间 | 总耗时 | RTF |
|-------|----------|---------|--------|-----|
| speech-denoise | ~17 分钟（2 个文件） | 48s | 80s | 0.08x |
| speech-isolate | ~5.8 分钟（1 个文件） | 90s | 135s | 0.39x |

> **Note:** `speech-isolate` 采用两阶段 pipeline：Demucs（人声分离）+ ClearerVoice MossFormer2（降噪）。GPU 时间为两阶段合计。更高的 RTF 反映了每个文件需顺序运行两个模型。

Modal [L4 GPU](https://modal.com/pricing) 每小时 $0.80，但他们每月赠送 **$30 额度**——相当于 37 小时 L4 GPU 时间。按 RTF 0.4x 算，**你可以处理超过 93 小时的音频，分文不花**。个人创作者或小型工作室，绰绰有余。

---

## 🙏 Acknowledgments

- [Modal](https://modal.com) — GPU 云基础设施
- [ClearerVoice-Studio](https://huggingface.co/samson-castalk/ClearerVoice-Studio) — 语音增强工具包（MossFormer2 模型）
- [Demucs](https://github.com/facebookresearch/demucs) — 音乐源分离模型（htdemucs_ft）
- [skills.sh](https://skills.sh) — 开放 Agent Skills 生态
- [ClawHub](https://clawhub.ai) — OpenClaw Skills 分发平台

---

## 🔧 Development

See [DEVELOPMENT.md](DEVELOPMENT.md) for details.
