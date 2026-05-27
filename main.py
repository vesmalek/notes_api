from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

app = FastAPI()

# DONE: The Pydantic models (create and update)

class NoteCreate(BaseModel):
    title: str
    content: str
    tag: str = "general"
    pinned: bool = False
    archived: bool = False

class NoteUpdate(BaseModel):
    title: str
    content: str
    tag: str = "general"
    pinned: bool = False
    archived: bool = False

# DONE: In-memory storage setup with auto-incrementing ID

notes: dict = []
next_id: int = 1

# DONE: Helper function for finding a note by ID

def find_note(note_id: int) -> dict | None:
    for note in notes:
        if note["id"] == note_id:
            return note
    return None

# TODO: POST /notes — create a note, return 201
# TODO: GET /notes/{note_id} — get one note, 404 if missing
# TODO: PUT /notes/{note_id} — full update, 404 if missing
# TODO: DELETE /notes/{note_id} — delete, 204 on success, 404 if missing

