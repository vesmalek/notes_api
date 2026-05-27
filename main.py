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

# TODO: In-memory storage setup with auto-incrementing ID

# TODO: Helper function for finding a note by ID

