from fastapi import FastAPI, Body, Request
from src.presentation.notes import note_router
from src.presentation.translator import word_router
from core.database import session

app = FastAPI()


@app.middleware("http")
async def count_activity(request: Request, next_call):
    session.zadd("url:activity", mapping={str(request.url): 1}, incr=True)
    session.zincrby("url:activity", 1, str(request.url))
    return await next_call(request)


app.include_router(note_router)
app.include_router(word_router)
