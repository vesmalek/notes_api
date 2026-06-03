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

notes = []
next_id: int = 1

# DONE: Helper function for finding a note by ID

def find_note(note_id: int) -> dict | None:
    for note in notes:
        if note["id"] == note_id:
            return note
    return None

# DONE: POST /notes — create a note, return 201
@app.post("/notes", status_code=201)
async def create_note(note: NoteCreate):
    global next_id

    new_note = {
        "id": next_id,
        **note.model_dump()
    }
    
    notes.append(new_note)

    next_id += 1
    return new_note

# DONE: GET /notes/{note_id} — get one note, 404 if missing

@app.get("/notes/{note_id}")
async def get_note(note_id: int):
    note = find_note(note_id)
    
    if not note:
        raise HTTPException(status_code=404, detail="Note not found!")
    
    return note

# TODO: Build the list endpoint only `GET /notes` — but build it properly. Check notes_api_brief.md for more details

# TODO: Implement the query params as specified in the briefing doc

@app.get("/notes")
async def get_notes(
    skip: int=0, 
    limit: int = 10,
    archived: bool = False,
    tag: str | None = None,
    pinned: bool | None = None,
    search: str | None = None 
):
    # Apply filters in this order: `archived` → `tag` → `pinned` → `search` → paginate last.
    if archived:
        return [note for note in notes if note["archived"]][skip: skip + limit]
    return notes[skip: skip + limit]


# DONE: PUT /notes/{note_id} — full update, 404 if missing
@app.put("/notes/{note_id}")
async def update_note(note_id: int, note: NoteUpdate):
    result = find_note(note_id)

    if not result:
        raise HTTPException(status_code=404, detail="Note not found!")
    
    result["title"] = note.title
    result["content"] = note.content
    result["tag"] = note.tag
    result["pinned"] = note.pinned
    result["archived"] = note.archived

    return result


# DONE: DELETE /notes/{note_id} — delete, 204 on success, 404 if missing

@app.delete("/notes/{note_id}")
async def delete_note(note_id: int):
    note = find_note(note_id)

    if not note:
        raise HTTPException(status_code=404, detail="Note not found!")
    
    notes.remove(note)

    return f"Note deleted successfully!"

