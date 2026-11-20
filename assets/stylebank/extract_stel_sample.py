#!/usr/bin/env python3
"""Extract formal and informal candidate sentences from the STEL formality sample.

Each of the 100 STEL tasks holds two sentence pairs; a pair is the same
content written once formally and once informally.

Rules:
- Keep tasks where at least ``--min-votes`` of 5 annotators agreed.
- Shuffle the pairs and split them in half: the first half gives its formal
  sentence, the second half its informal sentence. No pair gives both, so
  the two styles never share content.
- Output JSON mapping ``formal`` and ``informal`` to sentence lists.
"""

from __future__ import annotations

import argparse
import csv
import json
import random
from pathlib import Path

SENTENCE_COLUMNS = ("Anchor 1", "Anchor 2", "Alternative 1.1", "Alternative 1.2")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--stel-tsv",
        type=Path,
        default=Path("data/stel/quad_stel-dimension_formal-100_sample.tsv"),
    )
    parser.add_argument(
        "-o", "--output", type=Path, default=Path("data/stel/stel_output.json")
    )
    parser.add_argument("--min-votes", type=int, default=4)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def pairs_of_task(row: dict[str, str]) -> list[dict[str, str]]:
    """Return the two pairs of a task as ``{"formal": ..., "informal": ...}``.

    The task ID names the style of each sentence in column order, e.g.
    ``QQ_i-454-f-454_f-2482-i-2482--1`` is informal, formal, formal, informal.
    """
    styles = [part for part in row["ID"][3:].replace("_", "-").split("-") if part in ("i", "f")]
    names = {"f": "formal", "i": "informal"}
    sentences = [" ".join(row[column].split()) for column in SENTENCE_COLUMNS]
    return [
        {names[styles[0]]: sentences[0], names[styles[1]]: sentences[1]},
        {names[styles[2]]: sentences[2], names[styles[3]]: sentences[3]},
    ]


def extract_samples(stel_tsv: Path, min_votes: int, seed: int) -> dict[str, list[str]]:
    pairs: list[dict[str, str]] = []
    with stel_tsv.open("r", encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t", quoting=csv.QUOTE_NONE):
            if int(row["# Votes out of 5 for Correct Alternative"]) >= min_votes:
                pairs.extend(pairs_of_task(row))

    random.Random(seed).shuffle(pairs)
    half = len(pairs) // 2
    return {
        "formal": [pair["formal"] for pair in pairs[:half]],
        "informal": [pair["informal"] for pair in pairs[half:]],
    }


def main() -> None:
    args = parse_args()
    data = extract_samples(args.stel_tsv, args.min_votes, args.seed)
    args.output.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({style: len(texts) for style, texts in data.items()}))
    print(f"Wrote samples to: {args.output}")


if __name__ == "__main__":
    main()
