from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

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

notes = []
next_id: int = 1

def find_note(note_id: int) -> dict | None:
    for note in notes:
        if note["id"] == note_id:
            return note
    return None

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

@app.get("/notes/{note_id}")
async def get_note(note_id: int):
    note = find_note(note_id)
    
    if not note:
        raise HTTPException(status_code=404, detail="Note not found!")
    
    return note

@app.get("/notes")
async def get_notes(
    skip: int=0, 
    limit: int = 10,
    archived: bool = False,
    tag: str | None = None,
    pinned: bool | None = None,
    search: str | None = None 
):
    if archived:
        return [note for note in notes if note["archived"]][skip: skip + limit]
    
    if tag:
        return [note for note in notes if note["tag"] == tag][skip: skip + limit]

    if pinned:
        return [note for note in notes if note["pinned"]][skip: skip + limit]
    
    if search:
        search_results = []
        for note in notes:
            if search in note["title"] or search in note["content"] or search in note["tag"]:
                search_results.append(note)
        return search_results[skip: skip + limit]
    sorted_list = sorted(notes, key=lambda d: d['pinned'], reverse=True)
    return sorted_list[skip: skip + limit]

@app.put("/notes/{note_id}/pin")
async def pin_note(note_id: int):
    result = find_note(note_id)

    if not result:
        raise HTTPException(status_code=404, detail='Note not found!')
    elif not result['title'].strip() or not result['content'].strip():
        raise HTTPException(status_code=400, detail='Title or content missing')
    
    result['pinned'] = True

@app.put("/notes/{note_id}/unpin")
async def pin_note(note_id: int):
    result = find_note(note_id)

    if not result:
        raise HTTPException(status_code=404, detail='Note not found!')
    elif not result['title'].strip() or not result['content'].strip():
        raise HTTPException(status_code=400, detail='Title or content missing')
    
    result['pinned'] = False

@app.put("/notes/{note_id}/archive")
async def pin_note(note_id: int):
    result = find_note(note_id)

    if not result:
        raise HTTPException(status_code=404, detail='Note not found!')
    elif not result['title'].strip() or not result['content'].strip():
        raise HTTPException(status_code=400, detail='Title or content missing')
    
    result['archived'] = True

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

@app.delete("/notes/{note_id}")
async def delete_note(note_id: int):
    note = find_note(note_id)

    if not note:
        raise HTTPException(status_code=404, detail="Note not found!")
    
    notes.remove(note)

    return f"Note deleted successfully!"

