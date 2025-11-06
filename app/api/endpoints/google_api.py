from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_crud
from app.schemas.charity_project import CharityProjectDB
from app.services.google_api import (create_spreadsheets, set_user_permissions,
                                     update_spreadsheets_value)

router = APIRouter()


@router.post(
    '/',
    response_model=list[CharityProjectDB],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(current_superuser)],
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)
):
    """
    Создаёт отчёт в Google Sheets и возвращает отсортированный
    список закрытых проектов.
    """
    charity_projects = await charity_crud.get_projects_by_completion_rate(
        session
    )
    spreadsheetid = await create_spreadsheets(wrapper_services)
    await set_user_permissions(spreadsheetid, wrapper_services)
    await update_spreadsheets_value(
        spreadsheetid,
        charity_projects,
        wrapper_services,
    )
    return charity_projects
