from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class NoteBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, example="Project Roadmap")
    content: str = Field(
        ..., min_length=1, example="FastAPI implementation standards review."
    )


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = Field(None, min_length=1)


class NoteResponse(NoteBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)