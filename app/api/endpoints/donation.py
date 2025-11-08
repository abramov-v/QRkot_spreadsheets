from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import CharityProject
from app.models import User
from app.schemas.donation import (DonationAdminOut, DonationCreate,
                                  DonationUserOut)
from app.services.investing import invest

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationAdminOut],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary='Получить все пожертвования',
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Получить список всех пожертвований (только для суперпользователей)."""
    return await donation_crud.get_multi(session)


@router.post(
    '/',
    response_model=DonationUserOut,
    response_model_exclude_none=True,
    summary='Создать пожертвование',
)
async def create_donation(
    obj_in: DonationCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Создать новое пожертвование (для авторизованных пользователей)."""
    new_donation = await donation_crud.create(obj_in, session, user)
    await invest(new_donation, CharityProject, session)
    return new_donation


@router.get(
    '/my',
    response_model=list[DonationUserOut],
    response_model_exclude_none=True,
    summary='Получить пожертвования текущего пользователя',
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Получить список пожертвований текущего пользователя."""
    return await donation_crud.get_user_donations(user, session)
