<div align="center">

![banner](banner.jpg)

# Speech & Vocal Skills

**你的錄音，從此沒有噪音。**

住在嘈雜的公寓？功放有嗡嗡聲？頭頂有飛機飛過？
這個 Skill 來解決。幾秒鐘完成去噪——運行在 Modal L4 GPU 上，而且免費。

Built for ourselves. Open to everyone.

[🇺🇸 English](README.md) | [🇨🇳 简体中文](README_CN.md) | [🇹🇼 繁體中文](README_TW.md)

</div>

---

## 🎤 speech-denoise

你的錄音聽起來不錯，除了背景噪音。

不管是冷氣的嗡嗡聲、街上的車流、電流干擾，還是你的功放怎麼也去不掉的莫名雜音——運行這個 Skill，還你乾淨的音頻。

支援所有常見格式：`.m4a`、`.mp3`、`.mp4`、`.wav`、`.flac`、`.ogg`、`.aac`、`.mov`、`.avi`。

告訴你的 AI agent：
```bash
denoise these files: /path/to/file1, /path/to/file2...
```

不需要任何音頻編輯技能。

---

## 📦 Installation

```bash
npx skills add speech2srt/skills
```

使用 OpenClaw？直接告訴你的 agent：`install speech-denoise skill` 或 `install speech-isolate skill`。

---

## ✨ One more thing...

### 🎵 speech-isolate

**🎵 speech-isolate** — 從任何音軌中人聲提取。

有一首音樂想提取人聲？或者反過來要伴奏？這就是這個 Skill。

> **Tip:** 做 ASR 之前先用這個。背景音樂會干擾語音識別模型——先去音樂，再做識別，字幕更乾淨。

---

## 🚀 Performance

**L4 GPU on Modal — 實測數據：**

| Skill | 音頻時長 | GPU 時間 | 總耗時 | RTF |
|-------|----------|---------|--------|-----|
| speech-denoise | ~17 分鐘（2 個檔案） | 48s | 80s | 0.08x |
| speech-isolate | ~6 分鐘（1 個檔案） | 30s | 36s | 0.09x |

Modal [L4 GPU](https://modal.com/pricing) 每小時 $0.80，但他們每月贈送 **$30 額度**——相當於 37 小時 L4 GPU 時間。按保守 RTF 0.1x 算，**你可以處理超過 370 小時的音頻，分文不花**。個人創作者或小型工作室，綽綽有餘。

---

## 🙏 Acknowledgments

- [Modal](https://modal.com) — GPU 雲端基礎設施
- [ClearerVoice-Studio](https://huggingface.co/samson-castalk/ClearerVoice-Studio) — 語音增強工具包（MossFormer2 模型）
- [Demucs](https://github.com/facebookresearch/demucs) — 音樂源分離模型（htdemucs_ft）
- [skills.sh](https://skills.sh) — 開放 Agent Skills 生態
- [ClawHub](https://clawhub.ai) — OpenClaw Skills 分發平台

---

## 🔧 Development

See [DEVELOPMENT.md](DEVELOPMENT.md) for details.
