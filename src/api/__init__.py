import sqlalchemy as sa
from fastapi import FastAPI
from fastapi_utils.session import FastAPISessionMaker
from fastapi_utils.tasks import repeat_every

import src.api.protocols
from src.api import users, protocols
from src.database import DatabaseSettings, create_database_url
from src.user.service import UserService
from src.stats.service import StatService

db_settings = DatabaseSettings()
db_url = create_database_url(db_settings)
session_maker = FastAPISessionMaker(db_url)
engine = sa.create_engine(db_url, future=True)


def get_application() -> FastAPI:
    application = FastAPI(
        title="GitHub Repo Stats",
        description="Сервис сбора статистических данных о популярности репозиториев на GitHub.",
        version="1.0.0",
    )

    application.include_router(users.router)
    user_service = UserService(engine)
    application.dependency_overrides[protocols.UserServiceProtocol] = lambda: user_service
    return application


app = get_application()


@app.on_event("startup")
@repeat_every(seconds=60 * 60 * 24)  # once a day
async def scan_repos_task() -> None:
    service = StatService(engine)
    await service.scan()
