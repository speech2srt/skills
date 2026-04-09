---
name: vocal-denoise
description: Vocal/audio denoising pipeline using ClearVoice MossFormer2 on Modal L4 GPU. Use when user wants to denoise, enhance, or clean up audio files. Triggers include: "denoise these files", "去噪", "enhance audio", "remove noise from recording", "clean up this audio", "run the denoise pipeline". Takes local audio files, uploads to Modal volume, runs GPU inference, and downloads enhanced results.
---

# Vocal Denoise

Single-stage speech enhancement pipeline — ffmpeg conversion + ClearVoice MossFormer2 GPU inference in one Modal container.

**Pipeline code is bundled in this skill** at `./denoise.py` and `./src/`. After `npx skills add`, the skill is self-contained and can run from anywhere. This SKILL.md lives at the skill root; `./` refers to the skill root directory.

## Prerequisites

Before running, verify:

1. **Python 3.9+** — run `python -V` to check. If missing or version is below 3.9, tell user to install from python.org
2. **Modal CLI** — run `modal config show` to check:
   - If "command not found": install with `pip install modal`, then `modal setup`
   - If `token_id` is null or shows an error: run `modal setup` to authenticate
   - If `token_id` has a value: Modal is installed and authenticated

## Workflow

### 1. Prepare slug and identify files

A **slug** is the task identifier — used as the volume directory name.

- If user provides a slug: use it as-is
- If user does not provide a slug: generate from timestamp: `denoise_YYYYMMDD_HHMMSS`

If user provides a **directory path** (not a specific file):

1. Scan the directory for audio/video files — supported formats like `.m4a`, `.mp3`, `.mp4`, `.wav`, `.flac`, `.ogg`, `.aac`, `.mov`, `.avi`
2. List all found files with a numbered index:
   ```
   Found N audio/video files in <directory>:
   [1] file1.m4a
   [2] file2.mp4
   ...
   ```
3. Ask user: "Process all files, or specify which ones by number?"
4. User selects — proceed with the selected files

If user provides **specific files** — use those files directly, no listing needed.

### 2. Upload files to volume

First, ensure the volume exists (idempotent — safe to run even if already created):
```bash
modal volume create speech2srt-denoise-data 2>/dev/null || true
```

Upload files to `<slug>/upload/` on the `speech2srt-denoise-data` volume:
```bash
modal volume put speech2srt-denoise-data <local_file> <slug>/upload/
```

For multiple files, upload each one:
```bash
modal volume put speech2srt-denoise-data ./file1.m4a <slug>/upload/
modal volume put speech2srt-denoise-data ./file2.m4a <slug>/upload/
```

### 3. Run pipeline

The pipeline entry point is `./denoise.py`. Run from the skill root:

```bash
modal run ./denoise.py --slug <slug>
```

Stream all output directly to user — this runs in real time.

**If user presses Ctrl+C** during the run: stop the pipeline cleanly, report what was completed up to the interruption, and tell user they can re-run with the same slug to resume (files already in volume will be reused).

### 4. Download results

After success, download each enhanced file back to its **original directory** (the directory it was uploaded from).

For each original file, the output path is:
```
<original_directory>/<original_stem>_enhanced.wav
```

Download each file individually with the correct destination:
```bash
modal volume get speech2srt-denoise-data <slug>/output/<enhanced_file> <original_directory>/
```

For example, if a file was uploaded from `/path/to/source/rec.m4a`, the enhanced file `<slug>/output/rec_enhanced.wav` should be downloaded to `/path/to/source/rec_enhanced.wav`.

Preserve the original directory tree — do not flatten into a single `./results/` folder, unless the user explicitly specifies a different results directory.

### 4.5. Clean up

After all downloads are complete, delete the entire slug folder from the volume to free up space:

```bash
modal volume rm speech2srt-denoise-data <slug> --recursive
```

### 5. Report

First, check if `ffmpeg` is available locally (`which ffmpeg`). If yes, append this question to the end of the report:
```
Convert to another format? (e.g. .mp3, .m4a, different sample rate or bitrate)
```

Then output the summary:

```
Done. Processed N file(s), RTF: X.XXx

Results:
  - <enhanced_path>  (X.X MB)
```

## Error Handling

| Error | Action |
|-------|--------|
| Volume does not exist | Tell user to run: `modal volume create speech2srt-denoise-data` |
| Modal run failed (auth error) | Tell user to run `modal setup` to re-authenticate |
| Modal run failed (other) | Paste the Modal error output verbatim |
| No audio files found in upload | Report "no audio files found" and which files were skipped |
