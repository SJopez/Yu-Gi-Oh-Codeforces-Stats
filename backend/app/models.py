from sqlmodel import SQLModel, Field, Column, JSON
from typing import Any, Optional
from datetime import datetime
# import json

class User(SQLModel, table=True):
    handle : str = Field(default='', primary_key=True)
    rating : int | None
    max_rating : int | None
    solved_problems : int | None
    tags: list[Any] | None = Field(default_factory=list,sa_column=Column(JSON))
    contributions : int
    rank : str | None
    max_rank : str | None
    badges: list[str] | None = Field(default_factory=list,sa_column=Column(JSON))
    most_used_lang : str | None
    avatar : str 
    timestamp : Optional[datetime] | None
    match_card: str | None