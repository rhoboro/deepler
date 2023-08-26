from collections import Counter
from dataclasses import dataclass
from enum import Enum
from typing import Any

import deepl

from .configuration import Config
from .histogram import Histogram
from .word_splitter import WordSplitter


class CountTarget(Enum):
    source_text = "source_text"
    result_text = "result_text"


@dataclass(frozen=True)
class TranslationResult:
    source_lang: str
    target_lang: str
    source_text: str
    result_text: str


@dataclass(frozen=True)
class Result(TranslationResult):
    count_target: CountTarget
    count_lang: str
    counts: Counter
    total_counts: Counter


class Translator:
    def translate(
        self,
        text: str,
        config_file: str,
        source_lang: str,
        target_lang: str,
        count_lang: str,
        **options: Any,
    ) -> Result:
        result = self._translate(
            text=text, source_lang=source_lang, target_lang=target_lang, **options
        )

        if target_lang.split("-")[0] == count_lang:
            counts_text = result.result_text
            count_target = CountTarget.result_text
        else:
            counts_text = result.source_text
            count_target = CountTarget.source_text
            count_lang = source_lang

        config = Config.load(config_file)
        counter = Counter(
            word.lower()
            for word in WordSplitter.create(lang=count_lang, text=counts_text).split()
        )
        histogram = Histogram.load(config).update(counter)
        histogram.save()

        return Result(
            source_lang=result.source_lang,
            target_lang=result.target_lang,
            source_text=result.source_text,
            result_text=result.result_text,
            count_target=count_target,
            count_lang=count_lang,
            counts=counter,
            total_counts=histogram.counts,
        )

    def _translate(
        self,
        text: str,
        config: str,
        source_lang: str,
        target_lang: str,
        **options: Any,
    ) -> TranslationResult:
        raise NotImplementedError


class DeepLTranslator(Translator):
    def __init__(self, auth_key: str) -> None:
        self.translator = deepl.Translator(auth_key=auth_key)

    def _translate(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        **options: Any,
    ) -> TranslationResult:
        result = self.translator.translate_text(
            text, source_lang=source_lang, target_lang=target_lang, **options
        )
        return TranslationResult(
            source_lang=source_lang,
            target_lang=target_lang,
            source_text=text,
            result_text=result.text,
        )
