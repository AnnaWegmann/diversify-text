"""MIS-based content preservation filter.

Uses the `Mutual Implication Score <https://huggingface.co/s-nlp/Mutual_Implication_Score>`_
to score paraphrases against their originals and regenerate those that fall
below a content-preservation threshold.
"""

from __future__ import annotations

import logging
from collections.abc import Callable

logger = logging.getLogger(__name__)

_DEFAULT_MIN_SCORE = 0.70
_DEFAULT_MAX_ATTEMPTS = 3


class MISFilter:
    """Score paraphrases against originals using Mutual Implication Score.

    The model is loaded lazily on first use.

    Parameters
    ----------
    device : str, optional
        Torch device for the MIS model (e.g. ``"cpu"``, ``"cuda"``).
    min_score : float
        Minimum acceptable MIS score.  Paraphrases scoring below this
        are generated again.
    max_attempts : int
        How many times a paraphrase is generated at most, counting the
        first time.  A paraphrase is only generated again while it
        scores below *min_score*.
    """

    def __init__(
        self,
        device: str | None = None,
        *,
        min_score: float = _DEFAULT_MIN_SCORE,
        max_attempts: int = _DEFAULT_MAX_ATTEMPTS,
    ) -> None:
        from diversify_text._utils import default_device

        self.device = device or default_device()
        self.min_score = min_score  # validated by setter
        self.max_attempts = max_attempts  # validated by setter
        self._mis = None

    @property
    def min_score(self) -> float:
        return self._min_score

    @min_score.setter
    def min_score(self, value: float) -> None:
        if not (0 <= value <= 1):
            raise ValueError("min_score must be in [0, 1]")
        self._min_score = value

    @property
    def max_attempts(self) -> int:
        return self._max_attempts

    @max_attempts.setter
    def max_attempts(self, value: int) -> None:
        if value < 1:
            raise ValueError("max_attempts must be at least 1")
        self._max_attempts = value

    def prepare(self) -> None:
        """Pre-load the MIS model."""
        self._ensure_model()

    def _ensure_model(self):
        if self._mis is None:
            from mutual_implication_score import MIS

            from diversify_text._utils import suppress_hf_load_noise

            with suppress_hf_load_noise():
                logger.info("Loading MIS model on %s ...", self.device)
                self._mis = MIS(device=self.device)
            logger.info("MIS model loaded.")
        return self._mis

    def score(
        self,
        originals: list[str],
        paraphrases: list[str],
    ) -> list[float]:
        """Compute MIS scores for aligned (original, paraphrase) pairs.

        Re-implementation of ``MIS.compute()`` from
        `mutual_implication_score <https://github.com/s-nlp/mutual_implication_score/blob/b47c88e978f510b3dee1d4bde1f22b054c67ad62/mutual_implication_score/mis_wrapper.py#L38>`_.
        The upstream version crashes on NumPy ≥ 2.0 because
        ``model()`` returns shape ``(batch, 1)`` tensors, and after
        ``.cpu().numpy()`` + ``list.extend()`` each element is a 1-D
        array of shape ``(1,)`` on which ``float()`` raises
        ``TypeError: only 0-dimensional arrays can be converted to
        Python scalars``.

        Fix: added ``.flatten()`` before ``.tolist()`` so the tensor is
        squeezed to 1-D before conversion.

        Parameters
        ----------
        originals : list[str]
            Source texts, one per pair.
        paraphrases : list[str]
            Generated paraphrases, aligned 1:1 with *originals*.

        Returns
        -------
        list[float]
            MIS scores in [0, 1], one per pair.
        """
        if len(originals) != len(paraphrases):
            raise ValueError("originals and paraphrases must have the same length")
        import torch
        from torch.utils.data import DataLoader

        mis = self._ensure_model()

        # Follows the structure of MIS.compute():
        # https://github.com/s-nlp/mutual_implication_score/blob/b47c88e978f510b3dee1d4bde1f22b054c67ad62/mutual_implication_score/mis_wrapper.py#L38
        #
        # Changes from upstream:
        # - PairsDatasetInference replaced with list(zip(...)) (equivalent)
        # - merged_prob uses .flatten().tolist() instead of .cpu().numpy()
        #   followed by float(e), which crashes on NumPy ≥ 2.0.
        dataset_direct = list(zip(originals, paraphrases))
        dataloader_direct = DataLoader(dataset_direct, batch_size=16)
        dataset_reverse = list(zip(paraphrases, originals))
        dataloader_reverse = DataLoader(dataset_reverse, batch_size=16)

        preds = []
        for b1, b2 in zip(dataloader_direct, dataloader_reverse):
            with torch.no_grad():
                tokenized1 = mis.tokenizer(
                    *b1, padding=True, truncation="longest_first",
                    return_tensors="pt",
                ).to(mis.device)
                tokenized2 = mis.tokenizer(
                    *b2, padding=True, truncation="longest_first",
                    return_tensors="pt",
                ).to(mis.device)
                merged_prob = mis.model(tokenized1, tokenized2)
                merged_prob = torch.sigmoid(merged_prob)
            # upstream: merged_prob.cpu().numpy() then float(e) — crashes on
            # NumPy ≥ 2.0 because elements are shape-(1,) arrays.
            preds.extend(merged_prob.cpu().flatten().tolist())
        return preds

    def replace_low_scoring(
        self,
        originals: list[str],
        paraphrases_by_text: list[list[str]],
        regenerate: Callable[[list[tuple[int, int]]], list[str]],
    ) -> list[list[str]]:
        """Regenerate the paraphrases that score below *min_score*.

        Every paraphrase is scored once.  Those below *min_score* are
        generated again and scored again, until they reach *min_score*
        or have been generated *max_attempts* times.  A paraphrase that
        never reaches *min_score* is replaced by its best-scoring
        attempt.

        Parameters
        ----------
        originals : list[str]
            Original input texts.
        paraphrases_by_text : list[list[str]]
            The first paraphrases, shape ``[n_texts][n]``.
        regenerate : callable
            Takes a list of ``(text index, paraphrase index)`` pairs and
            returns one new paraphrase for each pair, in the same order.

        Returns
        -------
        list[list[str]]
            Shape ``[n_texts][n]``, with the same styles in the same
            places as *paraphrases_by_text*.
        """
        best = [list(row) for row in paraphrases_by_text]
        positions = [
            (text_idx, paraphrase_idx)
            for text_idx, row in enumerate(best)
            for paraphrase_idx in range(len(row))
        ]
        scores = self.score(
            [originals[text_idx] for text_idx, _ in positions],
            [best[text_idx][paraphrase_idx] for text_idx, paraphrase_idx in positions],
        )
        best_score = dict(zip(positions, scores))

        for _ in range(self.max_attempts - 1):
            below = [p for p in positions if best_score[p] < self.min_score]
            if not below:
                break
            logger.info(
                "MIS filter: regenerating %d/%d paraphrase(s) below %.2f.",
                len(below), len(positions), self.min_score,
            )
            new_paraphrases = regenerate(below)
            new_scores = self.score(
                [originals[text_idx] for text_idx, _ in below], new_paraphrases
            )
            for position, paraphrase, score in zip(below, new_paraphrases, new_scores):
                if score > best_score[position]:
                    text_idx, paraphrase_idx = position
                    best[text_idx][paraphrase_idx] = paraphrase
                    best_score[position] = score

        still_below = sum(score < self.min_score for score in best_score.values())
        if still_below:
            logger.warning(
                "MIS filter: %d/%d paraphrases remain below %.2f. "
                "Keeping best-scoring attempts.",
                still_below, len(positions), self.min_score,
            )
        return best
