from dataclasses import dataclass
from datetime import datetime

@dataclass
class Word:
    _english: str
    _spanish: str
    _entry_date: datetime
    _part_of_speech: str = None
    _category: str = None
    _repetition_date: datetime = None
    _knowledge_level: int = None

    @property
    def english(self) -> str:
        return self._english

    @english.setter
    def english(self, value: str) -> None:
        self._english = value

    @property
    def spanish(self) -> str:
        return self._spanish

    @spanish.setter
    def spanish(self, value: str) -> None:
        self._spanish = value

    @property
    def entry_date(self) -> datetime:
        return self._entry_date

    @entry_date.setter
    def entry_date(self, value: datetime) -> None:
        self._entry_date = value

    @property
    def category(self) -> str:
        return self._category

    @category.setter
    def category(self, value: str) -> None:
        self._category = value

    @property
    def repetition_date(self) -> datetime:
        return self._repetition_date

    @repetition_date.setter
    def repetition_date(self, value: datetime) -> None:
        self._repetition_date = value

    @property
    def part_of_speech(self) -> str:
        return self._part_of_speech

    @part_of_speech.setter
    def part_of_speech(self, value: str) -> None:
        self._part_of_speech = value

    @property
    def knowledge_level(self) -> int:
        return self._knowledge_level

    @knowledge_level.setter
    def knowledge_level(self, value: int) -> None:
        self._knowledge_level = value



