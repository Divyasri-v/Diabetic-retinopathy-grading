"""Optional: evaluate the trained model on YOUR labelled test images.

Creates the files that the "Model performance" page displays:
  evaluation/confusion_matrix.csv, classification_report.txt, metrics.json

Usage (Windows, from the project folder, with the virtual environment active):

  python scripts/evaluate_model.py --csv C:\\data\\test.csv --images C:\\data\\test_images

The CSV needs two columns (APTOS format): id_code, diagnosis   (diagnosis = 0..4)
Images are looked up as <images>/<id_code>.<ext> (png, jpg or jpeg).
Use the SAME 550 test images that produced the recorded 74.55% accuracy; any other set
will give different numbers.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from utils import config, prediction, preprocessing  # noqa: E402


def find_image(folder: Path, code: str):
    for ext in ("png", "jpg", "jpeg", "PNG", "JPG", "JPEG"):
        p = folder / f"{code}.{ext}"
        if p.is_file():
            return p
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv", required=True, help="CSV with columns id_code,diagnosis")
    ap.add_argument("--images", required=True, help="Folder containing the images")
    ap.add_argument("--output-dir", default=str(config.EVAL_DIR), help="Where to write results")
    ap.add_argument("--batch-size", type=int, default=16)
    args = ap.parse_args()

    from sklearn.metrics import classification_report, confusion_matrix, log_loss

    img_dir = Path(args.images)
    if not img_dir.is_dir():
        print(f"ERROR: images folder not found: {img_dir}")
        return 1

    if not Path(args.csv).is_file():
        print(f"ERROR: CSV file not found: {args.csv}")
        return 1
    with open(args.csv, newline="") as fh:
        rows = list(csv.DictReader(fh))
    if not rows or "id_code" not in rows[0] or "diagnosis" not in rows[0]:
        print("ERROR: the CSV must have the columns 'id_code' and 'diagnosis'.")
        return 1

    items, missing = [], 0
    for r in rows:
        p = find_image(img_dir, r["id_code"])
        if p is None:
            missing += 1
            continue
        items.append((p, int(r["diagnosis"])))
    if not items:
        print("ERROR: none of the images listed in the CSV were found in the images folder.")
        return 1
    if missing:
        print(f"WARNING: {missing} images listed in the CSV were not found and are skipped.")

    print("Loading model ...")
    model = prediction.get_model()

    y_true, probs = [], []
    for start in range(0, len(items), args.batch_size):
        chunk = items[start : start + args.batch_size]
        batch = []
        for path, label in chunk:
            try:
                batch.append(preprocessing.preprocess(preprocessing.load_image(path.read_bytes()))[0])
                y_true.append(label)
            except preprocessing.InvalidImageError as exc:
                print(f"  skipped {path.name}: {exc}")
        if batch:
            probs.append(prediction.predict_batch(model, np.stack(batch)))
        print(f"  {min(start + args.batch_size, len(items))}/{len(items)}", end="\r")
    print()

    probs = np.concatenate(probs)
    probs = probs / probs.sum(axis=1, keepdims=True)  # removes float rounding before log_loss
    y_true = np.array(y_true)
    y_pred = probs.argmax(axis=1)
    labels = list(range(config.NUM_CLASSES))

    cm = confusion_matrix(y_true, y_pred, labels=labels)
    names = [f"Grade {i} - {config.CLASS_NAMES[i]}" for i in labels]
    report = classification_report(y_true, y_pred, labels=labels, target_names=names, digits=3, zero_division=0)
    metrics = {
        "images_evaluated": int(len(y_true)),
        "accuracy": round(float((y_true == y_pred).mean()), 4),
        "loss": round(float(log_loss(y_true, probs, labels=labels)), 4),
        "pixel_scaling": config.PIXEL_SCALING,
        "resize_backend": config.RESIZE_BACKEND,
    }

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    np.savetxt(out / "confusion_matrix.csv", cm, fmt="%d", delimiter=",")
    (out / "classification_report.txt").write_text(report, encoding="utf-8")
    (out / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    print(report)
    print(metrics)
    print(f"Saved results to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
