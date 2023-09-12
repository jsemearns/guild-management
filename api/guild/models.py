from beanie import Document, Indexed

from ..models.timestamp import Timestamp


class GuildApplication(Timestamp):
    guild_id: Indexed(str)
    player_id: Indexed(str)
    is_approved: bool = False
    is_cancelled: bool = False

class Guild(Document):
    name: Indexed(str, unique=True)

class GuildInvite(Timestamp):
    guild_id: Indexed(str)
    player_id: Indexed(str)
    is_accepted: bool = False
    is_cancelled: bool = False
