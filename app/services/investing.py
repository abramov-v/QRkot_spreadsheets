from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation


def utcnow() -> datetime:
    """Вернуть текущее время в UTC."""
    return datetime.now(timezone.utc)


def is_closed(obj) -> bool:
    """Проверить, достиг ли объект полной суммы инвестиций."""
    return obj.invested_amount >= obj.full_amount


def close_obj(obj) -> None:
    """Закрыть объект если он полностью профинансирован."""
    if not obj.fully_invested and is_closed(obj):
        obj.fully_invested = True
        obj.close_date = utcnow()


def free_amount(obj) -> int:
    """Вычислить оставшуюся сумму доступную для инвестирования."""
    return max(0, obj.full_amount - obj.invested_amount)


def apply_transfer(donation: Donation, project: CharityProject) -> int:
    """Перераспределить средства между пожертвованием и проектом."""
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


async def invest(
    new_obj,
    counterpart_model,
    session: AsyncSession
) -> None:
    """Распределяет средства между новым объектом и записями второй модели."""
    if new_obj.fully_invested:
        return

    result = await session.execute(
        select(counterpart_model)
        .where(counterpart_model.fully_invested.is_(False))
        .order_by(
            counterpart_model.create_date.asc(),
            counterpart_model.id.asc(),
        )
    )
    counterparts = result.scalars().all()

    for counterpart in counterparts:
        if is_closed(new_obj):
            break

        if counterpart_model is CharityProject:
            apply_transfer(new_obj, counterpart)
        else:
            apply_transfer(counterpart, new_obj)

        session.add(counterpart)

    session.add(new_obj)
    await session.commit()
    await session.refresh(new_obj)
