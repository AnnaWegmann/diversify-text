"""Paraphrase two example texts into the first 20 styles of the default bank.

SMOKE=1 uses only the first 2 styles. Writes results/<run>/paraphrases.json.
"""
import json
import os
import pathlib
import subprocess
import time

from diversify_text import diversify

TEXTS = [
    "The experiment was conducted in a controlled lab setting.",
    "CLICK HERE to claim your FREE $500 gift card!!! Limited time offer, only today. "
    "Don't miss out, sign up now and WIN BIG!",
]
n = 2 if os.environ.get("SMOKE") == "1" else 20
sha = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True).strip()
run = pathlib.Path("results") / f"top20-{sha}-{time.strftime('%Y%m%d-%H%M%S')}"
run.mkdir(parents=True, exist_ok=True)
results = diversify(TEXTS, n=n)
(run / "paraphrases.json").write_text(json.dumps(results, indent=1, ensure_ascii=False))
(run / "metrics.json").write_text(json.dumps({"n_styles": n, "n_texts": len(TEXTS)}))
print(f"wrote {run}/paraphrases.json")
if n == 2:
    print("SMOKE OK")
