from typing import List, Optional
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.note import NoteModel
from app.schemas.note import NoteCreate, NoteUpdate


class NoteRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, note_in: NoteCreate) -> NoteModel:
        db_note = NoteModel(title=note_in.title, content=note_in.content)
        self.db.add(db_note)
        await self.db.flush()
        await self.db.refresh(db_note)
        return db_note

    async def get_by_id(self, note_id: str) -> Optional[NoteModel]:
        result = await self.db.execute(
            select(NoteModel).where(NoteModel.id == note_id)
        )
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[NoteModel]:
        result = await self.db.execute(
            select(NoteModel).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def update(self, note_id: str, note_in: NoteUpdate) -> Optional[NoteModel]:
        update_data = note_in.model_dump(exclude_unset=True)
        if not update_data:
            return await self.get_by_id(note_id)

        await self.db.execute(
            update(NoteModel).where(NoteModel.id == note_id).values(**update_data)
        )
        return await self.get_by_id(note_id)

    async def delete(self, note_id: str) -> bool:
        result = await self.db.execute(
            delete(NoteModel).where(NoteModel.id == note_id)
        )
        return result.rowcount > 0