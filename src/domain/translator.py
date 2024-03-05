from core.database import session
from src.presentation.DTO import WordDTO


class TranslatorService:
    async def count_word(self):
        print(len(session.keys("word:*")))
        return {"count": len(session.keys("word:*"))}

    async def add_translate(self, word: WordDTO):
        session.setnx(f"word:{word.eng}", word.ukr)
        return "OK"

    async def translate(self, word):
        return session.get(f"word:{word}")
