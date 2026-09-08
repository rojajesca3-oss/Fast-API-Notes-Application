from typing import List
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.note_repositories import NoteRepository
from app.schemas.note import NoteCreate, NoteUpdate, NoteResponse


class NoteService:

    def __init__(self, db: AsyncSession):
        self.repository = NoteRepository(db)

    async def create_note(self, note_in: NoteCreate) -> NoteResponse:
        db_note = await self.repository.create(note_in)
        return NoteResponse.model_validate(db_note)

    async def get_note_by_id(self, note_id: str) -> NoteResponse:
        db_note = await self.repository.get_by_id(note_id)
        if not db_note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Note with ID '{note_id}' not found.",
            )
        return NoteResponse.model_validate(db_note)

    async def list_notes(self, skip: int = 0, limit: int = 100) -> List[NoteResponse]:
        db_notes = await self.repository.get_all(skip=skip, limit=limit)
        return [NoteResponse.model_validate(note) for note in db_notes]

    async def update_note(self, note_id: str, note_in: NoteUpdate) -> NoteResponse:
        # Check existence first
        await self.get_note_by_id(note_id)
        updated_note = await self.repository.update(note_id, note_in)
        return NoteResponse.model_validate(updated_note)

    async def delete_note(self, note_id: str) -> None:
        # Check existence first
        await self.get_note_by_id(note_id)
        success = await self.repository.delete(note_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete note.",
            )