from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import (BaseUserManager, FastAPIUsers, IntegerIDMixin,
                           InvalidPasswordException)
from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport, JWTStrategy)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.constants import JWT_LIFETIME_SECONDS, MIN_PASSWORD_LENGTH
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """Возвращает асинхронную базу данных пользователей."""
    yield SQLAlchemyUserDatabase(session, User)

bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    """Стратегия JWT-аутентификации с заданным временем жизни токена."""
    return JWTStrategy(
        secret=settings.secret,
        lifetime_seconds=JWT_LIFETIME_SECONDS
    )


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """Управляет пользователями и выполняет валидацию при регистрации."""
    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        """Проверяет пароль на минимальную длину и отсутствие e-mail в нём."""
        if len(password) < MIN_PASSWORD_LENGTH:
            raise InvalidPasswordException(
                reason=f'Пароль должен содержать не менее '
                       f'{MIN_PASSWORD_LENGTH} символов'
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason='Пароль не должен содержать e-mail'
            )

    async def on_after_register(
            self, user: User, request: Optional[Request] = None
    ):
        pass


async def get_user_manager(user_db=Depends(get_user_db)):
    """Возвращает менеджер пользователей для FastAPI Users."""
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
