from typing import List

from pydantic import BaseModel

from ..guild.models import Guild


class GuildApplicationApproval(BaseModel):
    approved: bool

class UpdateGuildMemberRankRequest(BaseModel):
    rank_id: str

class CreateGuildRequest(BaseModel):
    guild: Guild

class UpdateRankPermissionRequest(BaseModel):
    permission_ids: List[str]
    guild_id: str