#!/bin/bash
# Pre-commit hook: sync skill bundle from project root
# Keeps skills/speech-denoise/denoise.py and src/ in sync with project root

set -e

SKILL_DIR="skills/speech-denoise"
SRC="denoise.py"
SRC_DIR="src"

# Only sync if skill directory exists
if [ ! -d "$SKILL_DIR" ]; then
 exit 0
fi

# Check Python syntax before committing
if [ -f "$SRC" ]; then
 python3 -m py_compile "$SRC" 2>/dev/null || { echo "Syntax error in $SRC, commit aborted"; exit 1; }
fi

# Sync main entry point
if [ -f "$SRC" ]; then
 cp -f "$SRC" "$SKILL_DIR/$SRC"
fi

# Sync src/ directory
if [ -d "$SRC_DIR" ]; then
 mkdir -p "$SKILL_DIR/$SRC_DIR"
 rsync -av --delete "$SRC_DIR/" "$SKILL_DIR/$SRC_DIR/"
fi

# Remove __pycache__ from skill bundle (required for ClawHub publishing)
if [ -d "$SKILL_DIR/src/__pycache__" ]; then
 rm -rf "$SKILL_DIR/src/__pycache__"
fi

# Clean all __pycache__ and .pyc files across the repo
find . -type d -name __pycache__ -not -path './.git/*' -exec rm -rf {} + 2>/dev/null || true
find . -name '*.pyc' -not -path './.git/*' -delete 2>/dev/null || true
