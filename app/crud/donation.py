from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.models.user import User


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


donation_crud = CRUDDonation(Donation)
