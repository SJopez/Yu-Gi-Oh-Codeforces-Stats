from sqlmodel import SQLModel, Field, Column, JSON
from typing import Any, Optional
from datetime import datetime, timezone
# import json

class User(SQLModel, table=True):
    handle : str = Field(default='', primary_key=True)
    rating : int 
    max_rating : int
    solved_problems : int | None
    tags: list[Any] | None = Field(default_factory=list,sa_column=Column(JSON))
    contributions : int
    rank : str
    max_rank : str
    badges: list[str] | None = Field(default_factory=list,sa_column=Column(JSON))
    most_used_lang : str | None
    avatar : str 
    rated_pos : int | None
    contr_pos : int | None
    timestamp : Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))