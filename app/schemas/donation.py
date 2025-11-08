from datetime import datetime
from typing import Optional

from pydantic import BaseModel, NonNegativeInt, PositiveInt


class DonationBase(BaseModel):
    """Базовая схема пожертвования."""
    full_amount: PositiveInt
    comment: Optional[str] = None

    class Config:
        extra = 'forbid'


class DonationCreate(DonationBase):
    """Схема для создания пожертвования."""


class DonationUserOut(DonationBase):
    """Схема пожертвования для пользователя."""
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationAdminOut(DonationUserOut):
    """Схема пожертвования для администратора."""
    user_id: int
    invested_amount: NonNegativeInt
    fully_invested: bool
    close_date: Optional[datetime] = None

    class Config:
        orm_mode = True
