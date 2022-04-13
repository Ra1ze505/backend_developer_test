from typing import List

from src.stats.models import StatUserResponseV1
from src.user.models import UserResponseV1, UserAddRequestV1


class UserServiceProtocol:
    def get_all_users(self) -> List[UserResponseV1]:
        raise NotImplementedError

    def get_user_by_id(self, id: int) -> UserResponseV1:
        raise NotImplementedError

    def add_user(self, user: UserAddRequestV1) -> None:
        raise NotImplementedError

    def delete_user_by_id(self, id: int) -> None:
        raise NotImplementedError

    def get_user_stats_by_id(self, id: int) -> StatUserResponseV1:
        raise NotImplementedError
