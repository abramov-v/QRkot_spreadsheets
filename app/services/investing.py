from datetime import datetime, timezone
from typing import Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.abstract import AbstractCharityDonation


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


def apply_transfer(
        object_1: AbstractCharityDonation,
        object_2: AbstractCharityDonation,
) -> int:
    """Переводит средства между двумя объектами.

    Закрывает заполненные и возвращает объем перевода.
    """
    if object_1.fully_invested or object_2.fully_invested:
        return 0
    take = min(free_amount(object_1), free_amount(object_2))
    if take <= 0:
        return 0
    object_1.invested_amount += take
    object_2.invested_amount += take
    close_obj(object_1)
    close_obj(object_2)
    return take


async def invest(
    new_obj: AbstractCharityDonation,
    counterpart_model: Type[AbstractCharityDonation],
    session: AsyncSession,
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
        apply_transfer(new_obj, counterpart)
        session.add(counterpart)

    session.add(new_obj)
    await session.commit()
    await session.refresh(new_obj)
