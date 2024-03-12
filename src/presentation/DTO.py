from dataclasses import dataclass
from enum import Enum
from typing import Literal


class CategoryEnum(Enum):
    news = 1
    economy = 2
    sport = 3


@dataclass
class WordDTO:
    eng: str
    ukr: str


@dataclass
class PostDTO:
    title: str
    owner_id: int
    category: str
    description: str = None
