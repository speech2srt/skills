# Development

Pipeline code lives at the repo root and is synced to `skills/` via pre-commit hook.

`pre-commit.sh` located at project root, this hook runs automatically on `git commit` (when properly symlinked):

**What it does:**
1. **Syntax check** — validates Python entry points (`denoise.py`, `isolate.py`) with `py_compile`
2. **Bundle sync** — copies entry points and `src/` directory into each skill bundle
3. **Cleanup** — removes `__pycache__` and `.pyc` files across the repo

**Setup (already done — for reference):**
```bash
# Create symlink to enable the hook
ln -sf ../../pre-commit.sh .git/hooks/pre-commit
```

**File structure:**
```
denoise.py          ← speech-denoise entry point
isolate.py          ← speech-isolate entry point
src/                ← config, images (synced to all skills)
skills/
├── speech-denoise/ ← bundled with denoise.py + src/
└── speech-isolate/ ← bundled with isolate.py + src/
```
