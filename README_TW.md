<div align="center">

![banner](banner.jpg)

# Speech & Vocal Skills

**你的錄音，從此沒有噪音。**

Built for ourselves. Open to everyone.

[🇺🇸 English](README.md) | [🇨🇳 简体中文](README_CN.md) | [🇹🇼 繁體中文](README_TW.md)

</div>

---

## 🎤 speech-denoise

你的錄音聽起來不錯，除了背景噪音。

冷氣嗡嗡聲、街上車流、電流干擾、功放的莫名雜音——執行這個 Skill，還你乾淨的音訊。

支援格式：`.m4a` `.mp3` `.mp4` `.wav` `.flac` `.ogg` `.aac` `.mov` `.avi`

```bash
denoise these files: /path/to/file1, /path/to/file2...
```

---

## 🎵 speech-isolate

提取錄音中的人聲。

錄音裡有背景音樂？這個人聲提取工具給你一條乾淨的人声音軌——沒有音樂、沒有噪音，可以直接用於轉寫。

---

## 🎙️ speech-transcribe

3x Faster than Whisper，語音轉文字，帶句級時間戳。

輸出兩種格式：純文字（`.txt`）用於文件，字幕檔（`.srt`）可直接匯入任何影片編輯器。

---

## 📦 Installation

```bash
npx skills add speech2srt/skills
```

或告訴你的 agent：`install speech-denoise`、`install speech-isolate` 或 `install speech-transcribe`。

---

## 🚀 Performance

**L4 GPU on Modal — 實測數據：**

| Skill | 音訊時長 | GPU 時間 | 總耗時 | RTF |
|-------|----------|---------|--------|-----|
| speech-denoise | ~17 分鐘（2 個檔案） | 48s | 80s | 0.08x |
| speech-isolate | ~5.8 分鐘（1 個檔案） | 90s | 135s | 0.39x |
| speech-transcribe | ~6 分鐘（1 個檔案，large-v3） | 70s | 75s | 0.19x |

> Modal [L4 GPU](https://modal.com/pricing) 每小時 $0.80，但他們每月贈送 **$30 額度**——相當於 37 小時 L4 GPU 時間。按 RTF 0.4x 算，**你可以處理超過 93 小時的音訊，分文不花**。個人創作者或小型工作室，綽綽有餘。

---

## 🙏 Acknowledgments

- [Modal](https://modal.com) — GPU 基礎設施
- [ClearerVoice-Studio](https://huggingface.co/samson-castalk/ClearerVoice-Studio) — MossFormer2
- [Demucs](https://github.com/facebookresearch/demucs) — 人聲分離
- [Whisper](https://github.com/openai/whisper) — 語音識別
- [faster-whisper](https://github.com/guillaumekln/faster-whisper) — 快速推理
- [skills.sh](https://skills.sh) — Skills 生態
- [ClawHub](https://clawhub.ai) — 分發平台

---

## 🔧 Development

See [DEVELOPMENT.md](DEVELOPMENT.md) for details.
