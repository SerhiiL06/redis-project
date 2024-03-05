from fastapi import APIRouter, Depends
from .DTO import WordDTO
from src.domain.translator import TranslatorService
from typing import Annotated

word_router = APIRouter(prefix="/word", tags=["translate"])


@word_router.post("")
async def add_translate(service: Annotated[TranslatorService, Depends()], dto: WordDTO):
    return await service.add_translate(dto)


@word_router.get("/count")
async def count_of_words(service: Annotated[TranslatorService, Depends()]):
    return await service.count_word()


@word_router.get("/{word}", summary="return the count of word in system")
async def translate_word(service: Annotated[TranslatorService, Depends()], word: str):
    return await service.translate(word)
