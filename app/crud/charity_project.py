from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    """CRUD класс для проектов."""
    async def charity_get_by_name(
            self,
            name: str,
            session: AsyncSession,
    ) -> Optional[CharityProject]:
        charity = await session.execute(
            select(CharityProject).where(
                CharityProject.name == name
            )
        )
        return charity.scalars().first()

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession,
    ):
        charity_days = (
            func.julianday(func.date(CharityProject.close_date)) -
            func.julianday(func.date(CharityProject.create_date))
        ).label('charity_days')

        result = await session.execute(
            select(CharityProject)
            .where(
                CharityProject.fully_invested.is_(True),
            )
            .order_by(
                charity_days.asc(),
                CharityProject.close_date.asc(),
                CharityProject.id.asc()),
        )
        return result.scalars().all()


charity_crud = CRUDCharityProject(CharityProject)
