from dataclasses import dataclass
from datetime import datetime

@dataclass
class Word:
    english: str
    spanish: str
    enter_date: datetime
    category: str = None
    repetition_date: datetime = None

    @property
    def english(self):
        return self.english

    @property
    def spanish(self):
        return self.spanish
