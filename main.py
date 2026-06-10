from pydantic import BaseModel, Field
from typing import Annotated
from fastapi import FastAPI, HTTPException, Query, Path

app = FastAPI()

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

class NoteFilters(BaseModel):
    skip: int = Field(0, ge=0)
    limit: int = Field(10, ge=1, le=100)
    archived: bool = False
    tag: str | None = Field(
        None,
        title='Tag',
        description='Keyword to filter notes by Tag',
        min_length=2,
        max_length=30
    )
    pinned: bool | None = None
    search: str | None = Field(
        None,
        title='Search',
        description='Keyword to find in note title',
        min_length=2,
        max_length=30
    )

notes = []
next_id: int = 1

def find_note(note_id: int) -> dict | None:
    for note in notes:
        if note["id"] == note_id:
            return note
    return None

@app.post("/notes", status_code=201)
async def create_note(note: NoteCreate):
    if not note.title.strip() or not note.content.strip():
        raise HTTPException(status_code=400, detail='Title/content is empty')
    
    global next_id

    new_note = {
        "id": next_id,
        **note.model_dump()
    }
    
    notes.append(new_note)

    next_id += 1
    return new_note

@app.get("/notes/{note_id}")
async def get_note(note_id: Annotated[int, Path(ge=1)]):
    note = find_note(note_id)
    
    if not note:
        raise HTTPException(status_code=404, detail="Note not found!")
    
    return note

@app.get("/notes")
async def get_notes(filters: Annotated[NoteFilters, Query()]):
    sorted_notes = sorted(notes, key=lambda d: d['pinned'], reverse=True)
    result = sorted_notes
    
    if not filters.archived:
        result = [n for n in result if not n['archived']]

    if filters.tag:
        result = [n for n in result if n['tag'] == filters.tag]

    if filters.pinned is not None:
        result = [n for n in result if n['pinned'] == filters.pinned]

    if filters.search:
        result = [n for n in result if filters.search.lower() in n['title'].lower()]

    return result[filters.skip: filters.skip + filters.limit]
    
@app.put("/notes/{note_id}/pin")
async def pin_note(note_id: Annotated[int, Path(ge=1)]):
    result = find_note(note_id)

    if not result:
        raise HTTPException(status_code=404, detail='Note not found!')
    
    result['pinned'] = True
    return result

@app.put("/notes/{note_id}/unpin")
async def unpin_note(note_id: Annotated[int, Path(ge=1)]):
    result = find_note(note_id)

    if not result:
        raise HTTPException(status_code=404, detail='Note not found!')
    
    result['pinned'] = False
    return result

@app.put("/notes/{note_id}/archive")
async def archive_note(note_id: Annotated[int, Path(ge=1)]):
    result = find_note(note_id)

    if not result:
        raise HTTPException(status_code=404, detail='Note not found!')
    
    result['archived'] = True
    return result

@app.put("/notes/{note_id}")
async def update_note(note_id: Annotated[int, Path(ge=1)], note: NoteUpdate):
    result = find_note(note_id)

    if not result:
        raise HTTPException(status_code=404, detail="Note not found!")
    
    if not note.title.strip() or not note.content.strip():
        raise HTTPException(status_code=400, detail='Title or content missing')
    
    result["title"] = note.title
    result["content"] = note.content
    result["tag"] = note.tag
    result["pinned"] = note.pinned
    result["archived"] = note.archived

    return result

@app.delete("/notes/{note_id}", status_code=204)
async def delete_note(note_id: Annotated[int, Path(ge=1)]):
    note = find_note(note_id)

    if not note:
        raise HTTPException(status_code=404, detail="Note not found!")
    
    notes.remove(note)
