---
name: ocr2markdown
description: "Document OCR and parsing — converts PDF/images to Markdown on remote L4 GPU. Trigger when user says: OCR, PDF to markdown, parse PDF, extract text from PDF, 文档识别, PDF转Markdown, 扫描件识别. Takes local PDF/image files and returns Markdown with structure preserved."
version: v1.0.0
---

# OCR2Markdown

MinerU document parsing pipeline on remote Modal GPU — PDF/image → Markdown with layout, tables, formulas, and OCR preserved.

**Pipeline code is bundled** at `./src/ocr2markdown.py`. After `npx skills add`, runs from any directory.

## Workflow

### 1. Prepare slug and identify files

**Slug** = task identifier (volume directory name). Use user-provided value, or generate `ocr_YYYYMMDD_HHMMSS` if none given.

**Directory input?** Scan for PDF (`.pdf`), list with index, ask user to confirm selection.

**Specific files?** Use directly, no listing needed.

### 2. Upload to volume

Ensure volume exists (idempotent):
```bash
modal volume create speech2srt-data 2>/dev/null || true
```

Upload each file:
```bash
modal volume put speech2srt-data <local_file> <slug>/upload/
```

Modal `put` auto-creates remote directories — no need to create `<slug>/upload/` manually.

### 3. Run pipeline

```bash
modal run ./src/ocr2markdown.py --slug <slug>
```

Stream output in real time.

**Ctrl+C?** Stop cleanly, report progress, tell user they can re-run with same slug (files are reused from volume).

### 4. Download results

Output directory structure:
```
<slug>/output/<stem>_ocr/
├── <stem>.md              # Main markdown output
├── images/                # Extracted images referenced by markdown
└── *.pdf, *.json          # Auxiliary outputs (layout, model data)
```

Download the entire output folder:
```bash
modal volume get speech2srt-data <slug>/output/ <local_destination>/
```

Preserve original directory tree — do not flatten into `./results/`.

### 5. Clean up

```bash
modal volume rm speech2srt-data <slug> --recursive
```

### 6. Report

Output:
```
Done. Parsed N PDF(s) in Xm Ys

Results:
  - <output_dir>/<stem>_ocr/<stem>.md
  - <output_dir>/<stem>_ocr/images/
```

## Setup

Before first run, verify:

1. **Python 3.9+** — `python -V`. Below 3.9 → tell user to install from python.org
2. **Modal CLI** — `modal config show`:
   - `token_id` null → `modal setup` to authenticate
   - command not found → `pip install modal` then `modal setup`

## Performance

| Document | Pages | GPU Time | CPU Time (local) |
|----------|-------|----------|-------------------|
| Small    | < 50  | ~1-2 min  | ~1-5 min         |
| Large   | 400+  | ~3-5 min  | ~1.5-2 hours     |

GPU (Modal L4) is **10-30x faster** than local CPU for large documents.

## Error Handling

See [references/error-handling.md](references/error-handling.md) for detailed error recovery.
