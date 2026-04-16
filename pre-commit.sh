#!/bin/bash
# Pre-commit hook: clean __pycache__ and .pyc files from all skills

set -e

find . -type d -name __pycache__ -not -path './.git/*' -exec rm -rf {} + 2>/dev/null || true
find . -type d -name '.mypy_cache' -not -path './.git/*' -exec rm -rf {} + 2>/dev/null || true
find . -name '*.pyc' -not -path './.git/*' -delete 2>/dev/null || true
find . -name '.pytest_cache' -not -path './.git/*' -exec rm -rf {} + 2>/dev/null || true
