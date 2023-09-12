from typing import Optional

from beanie import Document, Indexed


class Player(Document):
    user_id: str
    name: Optional[str]
    guild_id: Optional[str] = None
    rank_id: Optional[str] = None

class Rank(Document):
    name: str

class Permission(Document):
    name: str

class RankPermission(Document):
    rank_id: Indexed(str)
    permission_id: Indexed(str)
    guild_id: Indexed(str)