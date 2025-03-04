from typing import List

from sqlalchemy import select, insert, delete
from sqlalchemy.future import Engine

from src.database import tables
from src.stats.models import StatUserResponseV1, StatResponseV1
from src.user.models import UserResponseV1, UserAddRequestV1


class UserService:
    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    def get_all_users(self) -> List[UserResponseV1]:
        query = select(tables.users)
        with self._engine.connect() as connection:
            users_data = connection.execute(query)
        users = []
        for user_data in users_data:
            user = UserResponseV1(id=user_data["id"], login=user_data["login"], name=user_data["name"])
            users.append(user)
        return users

    def get_user_by_id(self, id: int) -> UserResponseV1:
        query = select(tables.users).where(tables.users.c.id == id)
        with self._engine.connect() as connection:
            user_data = connection.execute(query)
        user = UserResponseV1(id=user_data["id"], login=user_data["login"], name=user_data["name"])
        return user

    def add_user(self, user: UserAddRequestV1) -> None:
        query = insert(tables.users).values(id=user.id, login=user.login, name=user.name)
        with self._engine.connect() as connection:
            connection.execute(query)
            connection.commit()

    def delete_user_by_id(self, id: int) -> None:
        query = delete(tables.users).where(tables.users.c.id == id)
        with self._engine.connect() as connection:
            connection.execute(query)
            connection.commit()

    def get_user_stats_by_id(self, id: int, date_from: str, date_to: str) -> StatUserResponseV1:
        user_query = select(tables.users).where(tables.users.c.id == id)
        stats_query = select(tables.stats).where(tables.stats.c.user_id == id)
        if date_from:
            stats_query = stats_query.where(tables.stats.c.date >= date_from)
        if date_to:
            stats_query = stats_query.where(tables.stats.c.date <= date_to)
        with self._engine.connect() as connection:
            user_data = connection.execute(user_query).fetchone()
            stats_data = connection.execute(stats_query).fetchall()
        return StatUserResponseV1(
            user=UserResponseV1(**user_data),
            stats=[StatResponseV1(**data) for data in stats_data],
        )
