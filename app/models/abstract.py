from datetime import datetime, timezone

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.db import Base


class AbstractCharityDonation(Base):
    """Абстрактная модель для проектов и пожертвований."""

    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0, nullable=False)
    fully_invested = Column(Boolean, nullable=False, default=False)
    create_date = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    close_date = Column(DateTime, nullable=True)

    __table_args__ = (
        CheckConstraint('full_amount > 0', name='check_full_amount_positive'),
    )
