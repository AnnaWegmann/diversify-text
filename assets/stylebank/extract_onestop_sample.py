#!/usr/bin/env python3
"""Extract simple and complex paragraphs from the OneStopEnglish corpus.

The corpus holds 189 news articles, each rewritten by teachers at three
reading levels. The elementary version gives the ``simple`` paragraphs,
the advanced version (close to the original article) the ``complex`` ones.

Rules:
- Keep paragraphs with ``--min-words`` to ``--max-words`` words.
- Leave out paragraphs with quotations: quoted speech is the same at every level.
- ``simple``: per article, take the paragraph with the shortest sentences
  and the fewest long words; list the simplest first.
- ``complex``: per article, take the paragraph with the longest sentences
  and the most long words; list the most complex first.
- Keep up to ``--max-per-level`` paragraphs per level.
- Output JSON mapping ``simple`` and ``complex`` to paragraph lists.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

LONG_WORD_LETTERS = 7


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--corpus-dir", type=Path, default=Path("data/onestop"))
    parser.add_argument(
        "-o", "--output", type=Path, default=Path("data/onestop/onestop_output.json")
    )
    parser.add_argument("--min-words", type=int, default=40)
    parser.add_argument("--max-words", type=int, default=110)
    parser.add_argument("--max-per-level", type=int, default=64)
    return parser.parse_args()


def paragraphs_per_article(folder: Path, min_words: int, max_words: int) -> list[list[str]]:
    """Return, per article, its paragraphs (one per line) within the word limits
    and without quotations."""
    articles = []
    for path in sorted(folder.glob("*.txt")):
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        paragraphs = [" ".join(line.split()) for line in text.splitlines()]
        articles.append(
            [
                p
                for p in paragraphs
                if min_words <= len(p.split()) <= max_words and "“" not in p and '"' not in p
            ]
        )
    return articles


def difficulty(paragraph: str) -> float:
    """Words per sentence plus 60 times the share of long words; lower is simpler."""
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", paragraph) if s.strip()]
    words = re.findall(r"[A-Za-z’']+", paragraph)
    long_words = sum(len(word) >= LONG_WORD_LETTERS for word in words)
    return len(words) / len(sentences) + 60 * long_words / len(words)


def one_per_article(articles: list[list[str]], most_complex: bool) -> list[str]:
    """Take each article's simplest (or most complex) paragraph, ordered the same way."""
    pick = max if most_complex else min
    picked = {pick(paragraphs, key=difficulty) for paragraphs in articles if paragraphs}
    return sorted(picked, key=difficulty, reverse=most_complex)


def main() -> None:
    args = parse_args()
    limits = (args.min_words, args.max_words)
    elementary = paragraphs_per_article(args.corpus_dir / "Ele-Txt", *limits)
    advanced = paragraphs_per_article(args.corpus_dir / "Adv-Txt", *limits)
    data = {
        "simple": one_per_article(elementary, most_complex=False)[: args.max_per_level],
        "complex": one_per_article(advanced, most_complex=True)[: args.max_per_level],
    }
    args.output.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({style: len(texts) for style, texts in data.items()}))
    print(f"Wrote samples to: {args.output}")


if __name__ == "__main__":
    main()
