"""Shared fake DiversificationMethod implementations for tests."""

from diversify_text.method import DiversificationMethod


class PrefixMethod(DiversificationMethod):
    """Returns prefixed paraphrases: ``<prefix>:<text>:<i>``."""

    name = "prefix"

    def __init__(self, prefix: str) -> None:
        self.prefix = prefix

    def generate(self, texts, style_dict, *, max_new_tokens=None,
                 temperature=None, top_p=None, **kwargs):
        return [
            [f"{self.prefix}:{text}:{i}" for i in range(len(style_dict))]
            for text in texts
        ]


class FailingMethod(DiversificationMethod):
    """Always raises RuntimeError."""

    name = "failing"

    def generate(self, texts, style_dict, *, max_new_tokens=None,
                 temperature=None, top_p=None, **kwargs):
        raise RuntimeError("boom")


class CountingMethod(DiversificationMethod):
    """Counts generate() calls and returns ``<text>:<i>`` paraphrases."""

    name = "counting"

    def __init__(self) -> None:
        self.calls = 0

    def generate(self, texts, style_dict, *, max_new_tokens=None,
                 temperature=None, top_p=None, **kwargs):
        self.calls += 1
        return [
            [f"{text}:{i}" for i in range(len(style_dict))]
            for text in texts
        ]


class AttemptMethod(DiversificationMethod):
    """Returns different paraphrases on each generate() call.

    Output format: ``<text> (<style>, attempt <call>)``, so tests can tell
    which style and which generate() call a paraphrase came from.
    """

    name = "attempt"

    def __init__(self) -> None:
        self.attempt = 0

    def generate(self, texts, style_dict, *, max_new_tokens=None,
                 temperature=None, top_p=None, **kwargs):
        self.attempt += 1
        return [
            [f"{text} ({style}, attempt {self.attempt})" for style in style_dict]
            for text in texts
        ]
