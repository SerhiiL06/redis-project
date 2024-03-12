from typing import Annotated

from fastapi import APIRouter, Body, Depends, Response

from src.domain.notes import NoteService

note_router = APIRouter()


@note_router.post("/notes", status_code=201)
async def add_note(
    service: Annotated[NoteService, Depends()],
    user: int,
    note: str = Body(min_length=5),
):

    return await service.create_note(user, note)


@note_router.get("/notes", status_code=200)
async def user_notes(service: Annotated[NoteService, Depends()], user):
    return await service.user_notes(user)


@note_router.delete("/notes", status_code=204)
async def delete_note(
    service: Annotated[NoteService, Depends()], user: int, note_id: int
):
    return await service.drop_note(user, note_id)
