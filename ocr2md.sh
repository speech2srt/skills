#!/bin/bash
while [[ $# -gt 0 ]]; do
    case "$1" in
        --path)
            TARGET_DIR="$2"
            shift 2
            ;;
        *)
            shift
            ;;
    esac
done

if [ -z "$TARGET_DIR" ]; then
    echo "Usage: $0 --path <directory>"
    exit 1
fi

TARGET_DIR=$(cd "$TARGET_DIR" && pwd)

PDF_FILES=("$TARGET_DIR"/*.pdf)
if [ ${#PDF_FILES[@]} -eq 0 ] || [ ! -f "${PDF_FILES[0]}" ]; then
    echo "No .pdf files found in $TARGET_DIR"
    exit 0
fi

for PDF in "${PDF_FILES[@]}"; do
    BASENAME=$(basename "$PDF" .pdf)
    WORK_DIR="$TARGET_DIR/${BASENAME}_ocr"
    mkdir -p "$WORK_DIR"

    echo "==> Parsing: $BASENAME.pdf"
    mineru -p "$PDF" -o "$WORK_DIR" -b pipeline

    INNER_DIR="$WORK_DIR/$BASENAME"
    if [ -d "$INNER_DIR" ]; then
        mv "$INNER_DIR"/* "$WORK_DIR/" 2>/dev/null
        rmdir "$INNER_DIR"
    fi

    AUTO_DIR="$WORK_DIR/auto"
    if [ -d "$AUTO_DIR" ]; then
        mv "$AUTO_DIR"/* "$WORK_DIR/" 2>/dev/null
        rmdir "$AUTO_DIR"
    fi

    echo "  -> $WORK_DIR/"
done

echo "✅ Done"
