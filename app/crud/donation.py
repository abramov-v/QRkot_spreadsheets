from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject
from app.models.donation import Donation
from app.models.user import User
from app.services.investing import apply_transfer, is_closed


class CRUDDonation(CRUDBase):
    """CRUD класс для пожертвований."""
    async def get_user_donations(
            self,
            user: User,
            session: AsyncSession
    ) -> list[Donation]:

        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            ).order_by(Donation.create_date.desc())
        )
        return donations.scalars().all()

    async def invest_new_donation(
        self,
        donation: Donation,
        session: AsyncSession
    ) -> None:
        if donation.fully_invested:
            return

        result = await session.execute(
            select(CharityProject)
            .where(CharityProject.fully_invested.is_(False))
            .order_by(CharityProject.create_date.asc(),
                      CharityProject.id.asc())
        )
        projects = result.scalars().all()

        for project in projects:
            if is_closed(donation):
                break
            apply_transfer(donation, project)

        await session.commit()
        await session.refresh(donation)


donation_crud = CRUDDonation(Donation)
