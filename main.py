from fastapi import FastAPI, Body, Request
from core.database import session
from src.presentation.notes import note_router


app = FastAPI()


app.include_router(note_router)
