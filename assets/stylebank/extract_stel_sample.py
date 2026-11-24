#!/usr/bin/env python3
"""Extract formal/informal sentence pairs from the STEL formality sample.

Each of the 100 STEL tasks holds two sentence pairs; a pair is the same
content written once formally and once informally.

Rules:
- Keep tasks where at least ``--min-votes`` of 5 annotators agreed.
- Output a JSON list of pairs, each ``{"formal": ..., "informal": ...}``.
"""

from __future__ import annotations

import argparse
import csv
import json
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


def extract_pairs(stel_tsv: Path, min_votes: int) -> list[dict[str, str]]:
    pairs: list[dict[str, str]] = []
    with stel_tsv.open("r", encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t", quoting=csv.QUOTE_NONE):
            if int(row["# Votes out of 5 for Correct Alternative"]) >= min_votes:
                pairs.extend(pairs_of_task(row))
    return pairs


def main() -> None:
    args = parse_args()
    pairs = extract_pairs(args.stel_tsv, args.min_votes)
    args.output.write_text(json.dumps(pairs, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(pairs)} pairs to: {args.output}")


if __name__ == "__main__":
    main()
