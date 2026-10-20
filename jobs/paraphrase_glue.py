"""Paraphrase the GLUE sample with Gemma and record speed and GPU use.

Writes the paraphrases (.jsonl) and metrics.json to results/<run>/.
With SMOKE=1 only the first 5 texts are paraphrased.

    python jobs/paraphrase_glue.py data/glue100.tsv
"""

import csv
import json
import os
import statistics
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import torch
from transformers import AutoTokenizer

from diversify_text import Diversifier

MODEL = "google/gemma-4-E2B-it"
N_STYLES = 5
SMOKE = os.environ.get("SMOKE") == "1"

input_path = Path(sys.argv[1])
sha = subprocess.run(
    ["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True
).stdout.strip()
run_name = f"paraphrase_glue{'-smoke' if SMOKE else ''}-{sha}-{datetime.now():%Y%m%d-%H%M%S}"
run_dir = Path("results") / run_name
run_dir.mkdir(parents=True)

if SMOKE:
    with input_path.open(newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))[:5]
    input_path = run_dir / "glue5.tsv"
    with input_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)

# Sample GPU utilisation and memory once per second while the job runs.
# On MIG slices nvidia-smi may report utilisation as "[N/A]".
gpu_log = run_dir / "nvidia_smi.csv"
sampler = subprocess.Popen(
    [
        "nvidia-smi",
        "--query-gpu=timestamp,utilization.gpu,memory.used",
        "--format=csv,noheader,nounits",
        "-l", "1",
    ],
    stdout=gpu_log.open("w"),
    stderr=subprocess.DEVNULL,
)

try:
    diversifier = Diversifier(model=MODEL, device="cuda")
    start = time.perf_counter()
    diversifier._method.prepare()  # load the model now, to time it apart from generation
    load_seconds = time.perf_counter() - start

    torch.cuda.reset_peak_memory_stats()
    start = time.perf_counter()
    output_path = diversifier.diversify(
        str(input_path),  # diversify() does not accept Path objects
        n=N_STYLES,
        output_dir=run_dir,
        output_name="paraphrases",
    )
    generate_seconds = time.perf_counter() - start
    peak_memory_gb = torch.cuda.max_memory_allocated() / 1e9
finally:
    sampler.terminate()
    sampler.wait()

records = [json.loads(line) for line in Path(output_path).open()]
paraphrases = [p["text"] for r in records for p in r["paraphrases"]]
tokenizer = AutoTokenizer.from_pretrained(MODEL)
generated_tokens = sum(
    len(ids) for ids in tokenizer(paraphrases, add_special_tokens=False)["input_ids"]
)

utilisation, memory_used = [], []
for line in gpu_log.read_text().splitlines():
    fields = [field.strip() for field in line.split(",")]
    if len(fields) == 3 and fields[1].isdigit():
        utilisation.append(int(fields[1]))
    if len(fields) == 3 and fields[2].isdigit():
        memory_used.append(int(fields[2]))

metrics = {
    "model": MODEL,
    "smoke": SMOKE,
    "git_sha": sha,
    "gpu": torch.cuda.get_device_name(),
    "n_texts": len(records),
    "n_paraphrases": len(paraphrases),
    "load_seconds": round(load_seconds, 1),
    "generate_seconds": round(generate_seconds, 1),
    "seconds_per_text": round(generate_seconds / len(records), 2),
    "seconds_per_paraphrase": round(generate_seconds / len(paraphrases), 2),
    "generated_tokens": generated_tokens,
    "tokens_per_second": round(generated_tokens / generate_seconds, 1),
    "peak_torch_memory_gb": round(peak_memory_gb, 2),
    "gpu_utilisation_mean": round(statistics.mean(utilisation), 1) if utilisation else None,
    "gpu_utilisation_median": statistics.median(utilisation) if utilisation else None,
    "nvidia_smi_memory_used_max_mib": max(memory_used) if memory_used else None,
}
(run_dir / "metrics.json").write_text(json.dumps(metrics, indent=2))
print(json.dumps(metrics, indent=2))
print(f"Results in {run_dir}")
