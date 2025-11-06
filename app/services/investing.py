from datetime import datetime, timezone

from app.models.charity_project import CharityProject
from app.models.donation import Donation


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def is_closed(obj) -> bool:
    return obj.invested_amount >= obj.full_amount


def close_obj(obj) -> None:
    if not obj.fully_invested and is_closed(obj):
        obj.fully_invested = True
        obj.close_date = utcnow()


def free_amount(obj) -> int:
    return max(0, obj.full_amount - obj.invested_amount)


def apply_transfer(donation: Donation, project: CharityProject) -> int:
    if donation.fully_invested or project.fully_invested:
        return 0
    take = min(free_amount(donation), free_amount(project))
    if take <= 0:
        return 0
    project.invested_amount += take
    donation.invested_amount += take
    close_obj(project)
    close_obj(donation)
    return take
