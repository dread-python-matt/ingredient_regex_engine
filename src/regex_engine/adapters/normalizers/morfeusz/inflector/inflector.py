from morfeusz2 import Morfeusz

from regex_engine.adapters.normalizers.morfeusz.inflector.inflector_paradigm import (
    InflectionParadigm,
)
from regex_engine.adapters.normalizers.morfeusz.morfeusz_utils import (
    is_word_inflectionally_independent,
    tuples_to_generated_word,
)
from regex_engine.application.dto.base_word import BaseWord


class Inflector:
    def __init__(self, morfeusz: Morfeusz) -> None:
        self.morfeusz = morfeusz

    def prepare(self, word: BaseWord) -> InflectionParadigm:
        if is_word_inflectionally_independent(word):
            return InflectionParadigm(
                word=word,
                variations=[],
            )

        variations = tuples_to_generated_word(self.morfeusz.generate(word.lemma))
        return InflectionParadigm(word=word, variations=variations)
