from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.abstract import AbstractCharityDonation


class Donation(AbstractCharityDonation):
    """Модель пожертвования от пользователя."""
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(Text)
