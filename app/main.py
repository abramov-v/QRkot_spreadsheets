from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.api.routers import main_router
from app.core.config import settings
from app.core.init_db import create_first_superuser

app = FastAPI(title=settings.app_title)

app.include_router(main_router)


@app.get('/health', tags=['service'])
async def health():
    """health-check эндпоинт."""
    return {'status': 'ok'}


@app.get('/', include_in_schema=False)
async def index():
    """Редирект на Swagger."""
    return RedirectResponse(url='/docs')


@app.on_event('startup')
async def startup():
    """Создание суперпользователя при старте приложения."""
    await create_first_superuser()
