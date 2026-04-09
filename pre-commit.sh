#!/bin/bash
# Pre-commit hook: sync skill bundles from project root
# Keeps skills/speech-denoise/ and skills/speech-isolate/ in sync with project root

set -e

# ============================================================
# Skill bundles to sync
# ============================================================
SKILLS=("skills/speech-denoise" "skills/speech-isolate")

# ============================================================
# Source files to sync
# ============================================================
SRC_FILES=("denoise.py" "isolate.py")
SRC_DIR="src"

# ============================================================
# Check Python syntax for all entry points
# ============================================================
for src in "${SRC_FILES[@]}"; do
    if [ -f "$src" ]; then
        python3 -m py_compile "$src" 2>/dev/null || { echo "Syntax error in $src, commit aborted"; exit 1; }
    fi
done

# ============================================================
# Sync each skill bundle
# ============================================================
for skill_dir in "${SKILLS[@]}"; do
    # Only sync if skill directory exists
    if [ ! -d "$skill_dir" ]; then
        continue
    fi

    # Determine which entry point to use for this skill
    case "$skill_dir" in
        skills/speech-denoise)
            entry="denoise.py"
            ;;
        skills/speech-isolate)
            entry="isolate.py"
            ;;
        *)
            continue
            ;;
    esac

    # Sync entry point if it exists in root
    if [ -f "$entry" ]; then
        cp -f "$entry" "$skill_dir/$entry"
    fi

    # Sync src/ directory
    if [ -d "$SRC_DIR" ]; then
        mkdir -p "$skill_dir/$SRC_DIR"
        rsync -av --delete "$SRC_DIR/" "$skill_dir/$SRC_DIR/"
    fi

    # Remove __pycache__ from skill bundle (required for ClawHub publishing)
    if [ -d "$skill_dir/src/__pycache__" ]; then
        rm -rf "$skill_dir/src/__pycache__"
    fi
done

# ============================================================
# Clean all __pycache__ and .pyc files across the repo
# ============================================================
find . -type d -name __pycache__ -not -path './.git/*' -exec rm -rf {} + 2>/dev/null || true
find . -name '*.pyc' -not -path './.git/*' -delete 2>/dev/null || true
