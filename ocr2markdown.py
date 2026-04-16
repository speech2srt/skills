import modal
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
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


def _move_into(src: Path, dst_dir: Path):
    if src.name == "images" and (dst_dir / "images").exists():
        return
    dst = dst_dir / src.name
    if dst.exists():
        return
    shutil.move(str(src), str(dst))


def _flatten_and_save(work_dir: Path, stem: str):
    nested_pdf_dir = work_dir / stem
    if nested_pdf_dir.exists():
        for f in nested_pdf_dir.iterdir():
            if f.is_dir():
                if f.name == "auto":
                    for f2 in f.iterdir():
                        _move_into(f2, work_dir)
                else:
                    _move_into(f, work_dir)
            else:
                _move_into(f, work_dir)
        shutil.rmtree(nested_pdf_dir)
    nested_auto_dir = work_dir / "auto"
    if nested_auto_dir.exists():
        for f in nested_auto_dir.iterdir():
            _move_into(f, work_dir)
        shutil.rmtree(nested_auto_dir)


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
def ocr2markdown_single(pdf_path: str, slug: str, stem: str) -> dict:
    _bootstrap_cache()
    upload_dir = Path(config.MOUNT_DATA) / slug / config.DIR_UPLOAD
    output_base = Path(config.MOUNT_DATA) / slug / config.DIR_OUTPUT
    work_dir = output_base / f"{stem}_ocr"
    md_file = work_dir / f"{stem}.md"
    if md_file.exists():
        return {"pdf": stem, "elapsed": 0, "success": True, "error": None}
    work_dir.mkdir(parents=True, exist_ok=True)
    print(f"  [proc] {stem}.pdf")
    t1 = time.monotonic()
    res = subprocess.run(
        ["mineru", "-p", str(pdf_path), "-o", str(work_dir), "-b", "pipeline"],
        capture_output=True,
        text=True,
    )
    elapsed = time.monotonic() - t1
    if res.returncode != 0:
        print(f"    ERROR: {res.stderr[-500:]}")
        return {
            "pdf": stem,
            "elapsed": elapsed,
            "success": False,
            "error": res.stderr[-500:],
        }
    _flatten_and_save(work_dir, stem)
    if md_file.exists():
        print(f"    done in {elapsed:.1f}s")
        return {"pdf": stem, "elapsed": elapsed, "success": True, "error": None}
    return {
        "pdf": stem,
        "elapsed": elapsed,
        "success": False,
        "error": "md file not found",
    }


@images.app.local_entrypoint()
def main(slug: str, workers: int = 4, force: bool = False) -> None:
    upload_path = f"{slug}/{config.DIR_UPLOAD}"
    try:
        entries = images.volume_data.listdir(upload_path)
    except Exception as e:
        print(f"[ocr2markdown] failed to list {upload_path}: {e}")
        return
    pdf_entries = [
        e
        for e in entries
        if e.type == modal.volume.FileEntryType.FILE and e.path.lower().endswith(".pdf")
    ]
    if not pdf_entries:
        print(f"[ocr2markdown] no PDFs found in volume:{upload_path}")
        return
    pending = []
    for entry in pdf_entries:
        stem = Path(entry.path).stem
        if not force:
            try:
                images.volume_data.listdir(f"{slug}/{config.DIR_OUTPUT}/{stem}_ocr")
                print(f"  [skip] {stem}.pdf")
                continue
            except Exception:
                pass
        pdf_path = f"{config.MOUNT_DATA}/{entry.path}"
        pending.append((pdf_path, stem))
    if not pending:
        print("[ocr2markdown] all PDFs already processed")
        return
    print(f"[ocr2markdown] {len(pending)} PDF(s) with {workers} parallel containers")
    t0 = time.monotonic()
    results = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {
            ex.submit(ocr2markdown_single.remote, str(p), slug, s): s
            for p, s in pending
        }
        for future in as_completed(futures):
            stem = futures[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                results.append(
                    {"pdf": stem, "elapsed": 0, "success": False, "error": str(e)}
                )
    total_elapsed = time.monotonic() - t0
    ok = sum(1 for r in results if r["success"])
    print(f"\n[ocr2markdown] done. {ok}/{len(results)} in {total_elapsed:.1f}s")
