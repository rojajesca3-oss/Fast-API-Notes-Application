from typing import List
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.note import NoteCreate, NoteUpdate, NoteResponse
from app.services.note_service import NoteService

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.post(
    "/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED
)
async def create_note(
    note_in: NoteCreate, db: AsyncSession = Depends(get_db)
) -> NoteResponse:
    """Create a new note item."""
    service = NoteService(db)
    return await service.create_note(note_in)


@router.get("/", response_model=List[NoteResponse], status_code=status.HTTP_200_OK)
async def read_notes(
    skip: int = Query(0, ge=0, description="Pagination offset"),
    limit: int = Query(100, ge=1, le=500, description="Pagination limit"),
    db: AsyncSession = Depends(get_db),
) -> List[NoteResponse]:
    """Retrieve a paginated list of notes."""
    service = NoteService(db)
    return await service.list_notes(skip=skip, limit=limit)


@router.get(
    "/{note_id}", response_model=NoteResponse, status_code=status.HTTP_200_OK
)
async def read_note(
    note_id: str, db: AsyncSession = Depends(get_db)
) -> NoteResponse:
    """Retrieve a specific note by unique identifier string."""
    service = NoteService(db)
    return await service.get_note_by_id(note_id)


@router.patch(
    "/{note_id}", response_model=NoteResponse, status_code=status.HTTP_200_OK
)
async def update_note(
    note_id: str, note_in: NoteUpdate, db: AsyncSession = Depends(get_db)
) -> NoteResponse:
    """Partially update an existing note."""
    service = NoteService(db)
    return await service.update_note(note_id, note_in)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: str, db: AsyncSession = Depends(get_db)) -> None:
    """Delete a note by its identifier."""
    service = NoteService(db)
    await service.delete_note(note_id)
    return None