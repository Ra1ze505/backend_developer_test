from pydantic import BaseModel, Field
from datetime import datetime, date

from src.user.models import UserResponseV1


class StatCreateV1(BaseModel):
    repo_id: int = Field(..., alias="id")
    user_id: int = None
    date: datetime = Field(..., alias="created_at")
    stargazers: int = Field(..., alias="stargazers_count")
    forks: int
    watchers: int


class StatResponseV1(BaseModel):
    repo_id: int = Field(..., ge=1)
    date: date
    stargazers: int
    forks: int
    watchers: int


class StatUserResponseV1(BaseModel):
    user: UserResponseV1
    stats: list[StatResponseV1]
