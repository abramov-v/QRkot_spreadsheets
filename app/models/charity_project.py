from sqlalchemy import Column, String, Text

from app.models.abstract import AbstractCharityDonation


class CharityProject(AbstractCharityDonation):
    """Модель проекта для сбора пожертвований."""
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
