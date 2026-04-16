"""
Modal service: MinerU PDF-to-markdown pipeline on GPU.

Usage:
    modal run ocr2markdown.py --slug <slug>
"""

import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, "/root/src")
import ocr2md_config as config
import ocr2md_images as images


def _bootstrap_cache():
    models_dir = Path(config.MOUNT_MODELS)
    cache_dir = Path.home() / ".cache"
    if not cache_dir.is_symlink():
        if cache_dir.exists():
            shutil.rmtree(cache_dir)
        cache_dir.parent.mkdir(parents=True, exist_ok=True)
        cache_dir.symlink_to(models_dir, target_is_directory=True)
    models_dir.mkdir(parents=True, exist_ok=True)


@images.app.function(
    image=images.image_ocr2markdown,
    gpu=config.GPU_TYPE,
    volumes={
        config.MOUNT_DATA: images.volume_data,
        config.MOUNT_MODELS: images.volume_models,
    },
    timeout=config.TIMEOUT_OCR2MD,
    retries=0,
)
def ocr2markdown(slug: str) -> list[dict]:
    t0 = time.monotonic()

    _bootstrap_cache()

    upload_dir = Path(config.MOUNT_DATA) / slug / config.DIR_UPLOAD
    output_base = Path(config.MOUNT_DATA) / slug / config.DIR_OUTPUT

    pdf_files = sorted(upload_dir.glob("*.pdf"))
    if not pdf_files:
        return []

    print(f"[ocr2markdown] {len(pdf_files)} PDF(s) to process")

    results = []
    for pdf_path in pdf_files:
        basename = pdf_path.stem
        work_dir = output_base / f"{basename}_ocr"

        md_file = work_dir / f"{basename}.md"
        if md_file.exists():
            print(f"  Skipping: {basename}.pdf (already processed)")
            results.append({"pdf": pdf_path.name, "output_dir": str(work_dir)})
            continue

        work_dir.mkdir(parents=True, exist_ok=True)

        print(f"  Parsing: {basename}.pdf")

        result = subprocess.run(
            ["mineru", "-p", str(pdf_path), "-o", str(work_dir), "-b", "pipeline"],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            print(f"    ERROR: {result.stderr[-500:]}")
            continue

        inner_pdf_dir = work_dir / basename
        if inner_pdf_dir.exists():
            for f in inner_pdf_dir.iterdir():
                if f.is_dir():
                    if f.name == "auto":
                        for f2 in f.iterdir():
                            shutil.move(str(f2), str(work_dir))
                    else:
                        shutil.move(str(f), str(work_dir))
            shutil.rmtree(inner_pdf_dir)

        inner_auto_dir = work_dir / "auto"
        if inner_auto_dir.exists():
            for f in inner_auto_dir.iterdir():
                shutil.move(str(f), str(work_dir))
            shutil.rmtree(inner_auto_dir)

        md_file = work_dir / f"{basename}.md"
        if md_file.exists():
            print(f"    -> {work_dir}/")
            results.append({"pdf": pdf_path.name, "output_dir": str(work_dir)})

    images.volume_data.commit()

    elapsed = time.monotonic() - t0
    print(f"\n[ocr2markdown] done. {len(results)} file(s) in {elapsed:.1f}s")

    return results


@images.app.local_entrypoint()
def main(slug: str) -> None:
    ocr2markdown.remote(slug)
