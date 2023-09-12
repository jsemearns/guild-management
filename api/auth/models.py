from typing import Union

from beanie import Document
from pydantic import BaseModel


class User(Document):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None
