from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_exists,
                                check_charity_project_name_duplicate,
                                check_full_amount_not_less_than_invested,
                                check_project_has_no_investments_for_delete,
                                check_project_not_fully_invested)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_crud
from app.models import Donation
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investing import invest

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    summary='Получить все проекты',
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """Получить список всех проектов."""
    return await charity_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary='Создать проект',
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Создать новый проект (только для суперпользователей)."""
    await check_charity_project_name_duplicate(charity_project.name, session)
    new_charity_project = await charity_crud.create(charity_project, session)
    await invest(new_charity_project, Donation, session)
    return new_charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary='Удалить проект',
)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удалить проект (если нет инвестиций, только для суперпользователей)."""
    project = await check_charity_project_exists(project_id, session)
    await check_project_not_fully_invested(project)
    await check_project_has_no_investments_for_delete(project)
    return await charity_crud.remove(project, session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary='Обновить проект',
)
async def partially_update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Частично обновить проект (только для суперпользователей)."""
    project = await check_charity_project_exists(project_id, session)
    await check_project_not_fully_invested(project)

    if obj_in.name:
        await check_charity_project_name_duplicate(
            obj_in.name, session
        )

    if obj_in.full_amount is not None:
        await check_full_amount_not_less_than_invested(
            obj_in.full_amount, project
        )

    return await charity_crud.update(project, obj_in, session)
