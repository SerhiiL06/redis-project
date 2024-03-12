from datetime import datetime

from core.database import session


class NoteService:
    async def create_note(self, user: int, note: str):
        incr = session.incr("user_id_counter")
        key = f"note:{incr}"
        session.hset(key, mapping={"note": note, "created": str(datetime.now())})
        session.lpush(user, key)
        return {"ok": str(key)}

    async def user_notes(self, user: int):
        response = []
        for el in session.lrange(user, 0, -1):
            response.append(session.hgetall(el))
        return response

    async def drop_note(self, user: int, note_id):
        note = f"note:{note_id}"
        check = session.lrem(user, 0, f"note:{note_id}")

        if check < 1:
            return {"error": "permission danied"}

        session.delete(note)
        return {"ok": "delete success"}
