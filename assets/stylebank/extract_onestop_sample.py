#!/usr/bin/env python3
"""Extract simple and complex paragraphs from the OneStopEnglish corpus.

The corpus holds 189 news articles, each rewritten by teachers at three
reading levels. The elementary version gives the ``simple`` paragraphs,
the advanced version (close to the original article) the ``complex`` ones.

Rules:
- Keep paragraphs with ``--min-words`` to ``--max-words`` words.
- Take one random paragraph per article and level, so no article dominates.
- Keep up to ``--max-per-level`` paragraphs per level.
- Output JSON mapping ``simple`` and ``complex`` to paragraph lists.
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

LEVEL_FOLDERS = {"simple": "Ele-Txt", "complex": "Adv-Txt"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--corpus-dir", type=Path, default=Path("data/onestop"))
    parser.add_argument(
        "-o", "--output", type=Path, default=Path("data/onestop/onestop_output.json")
    )
    parser.add_argument("--min-words", type=int, default=40)
    parser.add_argument("--max-words", type=int, default=110)
    parser.add_argument("--max-per-level", type=int, default=64)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def paragraphs_of_article(path: Path, min_words: int, max_words: int) -> list[str]:
    """Return the article's paragraphs (one per line) within the word limits."""
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    paragraphs = [" ".join(line.split()) for line in text.splitlines()]
    return [p for p in paragraphs if min_words <= len(p.split()) <= max_words]


def extract_samples(
    corpus_dir: Path, min_words: int, max_words: int, max_per_level: int, seed: int
) -> dict[str, list[str]]:
    rng = random.Random(seed)
    samples: dict[str, list[str]] = {}
    for style, folder in LEVEL_FOLDERS.items():
        one_per_article = []
        for path in sorted((corpus_dir / folder).glob("*.txt")):
            paragraphs = paragraphs_of_article(path, min_words, max_words)
            if paragraphs:
                one_per_article.append(rng.choice(paragraphs))
        rng.shuffle(one_per_article)
        samples[style] = one_per_article[:max_per_level]
    return samples


def main() -> None:
    args = parse_args()
    data = extract_samples(
        args.corpus_dir, args.min_words, args.max_words, args.max_per_level, args.seed
    )
    args.output.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({style: len(texts) for style, texts in data.items()}))
    print(f"Wrote samples to: {args.output}")


if __name__ == "__main__":
    main()
