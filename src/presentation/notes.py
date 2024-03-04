from fastapi import APIRouter, Response, Body
from core.database import session
from datetime import datetime
import json

note_router = APIRouter()


@note_router.post("/notes")
async def add_note(user: int, note: str = Body()):
    incr = session.incr("user_id_counter")
    key = f"note:{incr}"
    session.hset(key, mapping={"note": note, "created": str(datetime.now())})
    session.lpush(user, key)
    return Response(str(key), 200)


@note_router.get("/notes")
async def get_user_notes(user):
    response = []

    for el in session.lrange(user, 0, -1):
        response.append(session.hgetall(el))
    return response
