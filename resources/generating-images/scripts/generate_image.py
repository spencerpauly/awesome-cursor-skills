#!/usr/bin/env python3
"""
Generate or edit images via OpenAI's gpt-image-2 model.

This script ALWAYS uses gpt-image-2. There is no fallback model and no way
to override it. If anything goes wrong (missing key, missing package, API
error, etc.) it exits immediately with a non-zero status. Do not silently
recover.

Usage:
  # Single image from prompt
  generate_image.py --prompt "a serene winter landscape" --out ./out.png

  # Edit / use one or more reference images (also requires a prompt)
  generate_image.py --prompt "make it look like a watercolor painting" \\
      --image ./photo.png --out ./out.png

  generate_image.py --prompt "combine these into a flat-lay product shot" \\
      --image ./a.png --image ./b.png --image ./c.png --out ./combined.png

  # Batch / parallel mode: run many distinct jobs concurrently
  generate_image.py --batch ./jobs.json --concurrency 5

  # Optional knobs
  --size 1024x1024 | 1536x1024 | 1024x1536 | 2048x2048 | 3840x2160 | auto
  --quality low | medium | high | auto
  --format png | jpeg | webp
  --n 1                       # variations of the SAME prompt in one call
  --concurrency 4             # parallel workers in --batch mode

Batch file format (JSON array of jobs):
  [
    {
      "prompt": "...",
      "out": "./a.png",
      "size": "1024x1024",
      "quality": "high",
      "format": "png",
      "n": 1,
      "image": ["./ref1.png", "./ref2.png"],
      "mask": "./mask.png"
    },
    { "prompt": "...", "out": "./b.png" }
  ]

Each job uses the same defaults as the single-shot CLI when fields are omitted.

Requires: OPENAI_API_KEY in env, and `pip install openai>=1.x`.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

MODEL = "gpt-image-2"

_print_lock = threading.Lock()


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Generate or edit images with OpenAI gpt-image-2. "
                    "Always uses gpt-image-2; fails fast on any error."
    )
    p.add_argument("--prompt", help="Text prompt describing the image. Required unless --batch is used.")
    p.add_argument(
        "--image",
        action="append",
        default=[],
        help="Path to a reference image. Pass multiple times for multiple inputs. "
             "If provided, uses the edits endpoint.",
    )
    p.add_argument("--mask", help="Optional mask PNG (must match first image size, with alpha channel).")
    p.add_argument("--out", default="./image.png", help="Output file path. For --n>1, an index suffix is added.")
    p.add_argument("--size", default="auto", help="Image size, e.g. 1024x1024 or 'auto'.")
    p.add_argument("--quality", default="auto", choices=["low", "medium", "high", "auto"])
    p.add_argument("--format", dest="output_format", default="png", choices=["png", "jpeg", "webp"])
    p.add_argument("--n", type=int, default=1, help="Number of variations of the same prompt to generate in one call.")
    p.add_argument(
        "--batch",
        help="Path to a JSON file describing multiple jobs. Each job runs in parallel. "
             "Mutually exclusive with --prompt/--image/--mask/--out.",
    )
    p.add_argument(
        "--concurrency",
        type=int,
        default=4,
        help="Max parallel workers in --batch mode (default 4).",
    )
    return p.parse_args()


def die(msg: str, code: int = 1) -> "None":
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def write_image(b64: str, out_path: Path, idx: int, total: int) -> Path:
    if total > 1:
        out_path = out_path.with_name(f"{out_path.stem}_{idx + 1}{out_path.suffix}")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(base64.b64decode(b64))
    return out_path


def run_job(client: Any, job: dict) -> list[Path]:
    """Run a single image job and return the written paths."""
    prompt = job.get("prompt")
    if not prompt:
        raise ValueError("job missing 'prompt'")

    out = job.get("out", "./image.png")
    size = job.get("size", "auto")
    quality = job.get("quality", "auto")
    output_format = job.get("format", "png")
    n = int(job.get("n", 1))
    images = job.get("image") or []
    if isinstance(images, str):
        images = [images]
    mask = job.get("mask")

    common: dict[str, Any] = {
        "model": MODEL,
        "prompt": prompt,
        "size": size,
        "quality": quality,
        "n": n,
    }
    if output_format != "png":
        common["output_format"] = output_format

    open_files: list = []
    try:
        if images:
            files = [open(p, "rb") for p in images]
            open_files.extend(files)
            kwargs = dict(common, image=files if len(files) > 1 else files[0])
            if mask:
                mf = open(mask, "rb")
                open_files.append(mf)
                kwargs["mask"] = mf
            result = client.images.edit(**kwargs)
        else:
            result = client.images.generate(**common)
    finally:
        for f in open_files:
            try:
                f.close()
            except Exception:
                pass

    out_base = Path(out)
    written: list[Path] = []
    for idx, item in enumerate(result.data):
        b64 = item.b64_json
        if not b64:
            raise RuntimeError(f"image {idx} for out={out} returned no b64_json payload.")
        written.append(write_image(b64, out_base, idx, len(result.data)))

    if not written:
        raise RuntimeError(f"API returned no images for out={out}.")
    return written


def main() -> int:
    args = parse_args()

    if not os.environ.get("OPENAI_API_KEY"):
        die("OPENAI_API_KEY is not set in the environment. Aborting.", code=2)

    try:
        from openai import OpenAI
    except ImportError:
        die("openai package not installed. Run: pip install --upgrade openai", code=2)

    client = OpenAI()

    if args.batch:
        if args.prompt or args.image or args.mask:
            die("--batch is mutually exclusive with --prompt/--image/--mask.", code=2)
        try:
            jobs = json.loads(Path(args.batch).read_text())
        except Exception as e:
            die(f"failed to read --batch file {args.batch}: {e}", code=2)
        if not isinstance(jobs, list) or not jobs:
            die("--batch file must contain a non-empty JSON array of job objects.", code=2)

        concurrency = max(1, int(args.concurrency))
        all_paths: list[Path] = []
        first_error: BaseException | None = None

        with ThreadPoolExecutor(max_workers=concurrency) as ex:
            futures = {ex.submit(run_job, client, job): i for i, job in enumerate(jobs)}
            for fut in as_completed(futures):
                i = futures[fut]
                try:
                    paths = fut.result()
                except BaseException as e:
                    if first_error is None:
                        first_error = e
                    with _print_lock:
                        print(f"ERROR: job {i} failed: {e}", file=sys.stderr)
                    continue
                with _print_lock:
                    for path in paths:
                        print(str(path.resolve()))
                all_paths.extend(paths)

        if first_error is not None:
            return 1
        if not all_paths:
            die("batch produced no images.")
        return 0

    if not args.prompt:
        die("--prompt is required (or use --batch).", code=2)

    job = {
        "prompt": args.prompt,
        "out": args.out,
        "size": args.size,
        "quality": args.quality,
        "format": args.output_format,
        "n": args.n,
        "image": list(args.image),
        "mask": args.mask,
    }
    try:
        written = run_job(client, job)
    except Exception as e:
        die(str(e))

    for path in written:
        print(str(path.resolve()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
