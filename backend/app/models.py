from sqlmodel import SQLModel, Field, Column, JSON
# import json

class User(SQLModel, table=True):
    handle : str = Field(default='', primary_key=True)
    rating : int 
    max_rating : int
    solved_problems : int
    tags: list[str] = Field(default='[]',sa_column=Column(JSON))
    contributions : int
    rank : str
    max_rank : str
    badges: list[str] = Field(default='[]',sa_column=Column(JSON))
    most_used_lang : str
    avatar : str
    rated_pos : int
    contr_pos : int