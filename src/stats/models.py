from pydantic import BaseModel, Field
from datetime import datetime


class StatCreateV1(BaseModel):
    repo_id: int = Field(..., alias="id")
    user_id: int = None
    date: datetime = Field(..., alias="updated_at")
    stargazers: int = Field(..., alias="stargazers_count")
    forks: int
    watchers: int
