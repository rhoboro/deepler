from collections.abc import Iterable

from deepler.constants import SOURCE_LANGS, TARGET_LANGS


class WordSplitter:
    def __init__(self, lang: str, text: str) -> None:
        self.lang = lang
        self.text = text

    def split(self) -> Iterable[str]:
        raise NotImplementedError

    @classmethod
    def create(cls, lang: str, text: str) -> "WordSplitter":
        if lang in SOURCE_LANGS + TARGET_LANGS:
            return DefaultSplitter(lang, text)

        return DefaultSplitter(lang, text)


class DefaultSplitter(WordSplitter):
    def split(self) -> Iterable[str]:
        for word in "".join(c if c.isalnum() else " " for c in self.text).split(" "):
            if word.isalnum() and not word.isnumeric():
                yield word
