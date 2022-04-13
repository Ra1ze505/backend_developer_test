import aiohttp
from sqlalchemy import insert, select
from sqlalchemy.engine import Engine

from src.user.service import UserService
from src.database import tables
from .consts import GITHUB_USER_REPOS_URL
from .models import StatCreateV1


class StatService:
    def __init__(self, engine: Engine) -> None:
        print("StatService init")
        self._engine = engine
        self._user_service = UserService(engine)

    async def scan(self):
        users = self._user_service.get_all_users()
        user_stats = await self.get_stats([(user.login, user.id) for user in users])
        self.bulk_insert_stats(user_stats)

    async def get_stats(self, user_info: list[str, id]) -> list[StatCreateV1]:
        result = []
        async with aiohttp.ClientSession() as session:
            for user_login, user_id in user_info:
                async with session.get(GITHUB_USER_REPOS_URL.format(login=user_login)) as resp:
                    if resp.status == 200:
                        parsed_json = await resp.json()
                        repos = [StatCreateV1(user_id=user_id, **repo) for repo in parsed_json]
                        result.extend(repos)
        return result

    def bulk_insert_stats(self, stats: list[StatCreateV1]) -> None:
        insert_values = self._get_insert_values(stats, self._get_existing_ids())
        with self._engine.connect() as conn:
            insert_query = insert(tables.stats).values(insert_values)
            conn.execute(insert_query)
            conn.commit()

    def _get_insert_values(self, stats: list[StatCreateV1], ids: set[int]) -> list[dict]:
        insert_values = []
        for stat in stats:
            if stat.repo_id not in ids:
                insert_values.append(stat.dict())
        return insert_values

    def _get_existing_ids(self) -> set[int]:
        with self._engine.connect() as conn:
            select_query = select([tables.stats.c.repo_id])
            return {i[0] for i in conn.execute(select_query).fetchall()}
