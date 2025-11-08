from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, NonNegativeInt, PositiveInt


class CharityProjectBase(BaseModel):
    """Базовая схема проекта."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt] = None

    class Config:
        extra = 'forbid'


class CharityProjectCreate(CharityProjectBase):
    """Схема для создания проекта."""
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):
    """Схема для обновления проекта."""


class CharityProjectDB(CharityProjectCreate):
    """Схема проекта для чтения из БД."""
    id: int
    invested_amount: NonNegativeInt
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = None

    class Config:
        orm_mode = True
