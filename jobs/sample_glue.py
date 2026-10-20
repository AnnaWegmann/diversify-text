"""Write a fixed sample of 100 GLUE validation texts to a TSV file.

Takes 25 texts each from SST-2, CoLA, MRPC and RTE, so the sample
mixes short and long texts.  Run once on the login node:

    uv run --managed-python --with datasets python jobs/sample_glue.py data/glue100.tsv
"""

import csv
import random
import sys
from pathlib import Path

from datasets import load_dataset

# GLUE task -> column holding the text to paraphrase
TASKS = {"sst2": "sentence", "cola": "sentence", "mrpc": "sentence1", "rte": "sentence1"}
PER_TASK = 25
SEED = 51173

out_path = Path(sys.argv[1])
out_path.parent.mkdir(parents=True, exist_ok=True)
rng = random.Random(SEED)
rows = []
for task, column in TASKS.items():
    texts = load_dataset("nyu-mll/glue", task, split="validation")[column]
    for text in rng.sample(texts, PER_TASK):
        rows.append({"task": task, "text": text})

with out_path.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["task", "text"], delimiter="\t")
    writer.writeheader()
    writer.writerows(rows)
print(f"Wrote {len(rows)} texts to {out_path}")
