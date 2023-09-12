import os
from typing import Any, List

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from .auth.models import User
from .auth.utils import get_password_hash
from .player.models import Permission, Player, Rank, RankPermission
from .utils.constants import PERMISSIONS, RANKS


async def init_db(document: str, models: List[Any]) -> None:
    # initialize collections
    client = AsyncIOMotorClient(f'mongodb://{os.environ.get("DB_URL")}:27017')
    if os.environ.get('DB_USE_AUTH'):
        client = AsyncIOMotorClient(f'mongodb://{os.environ.get("DB_USER_NAME")}:{os.environ.get("DB_PASSWORD")}@{os.environ.get("DB_URL")}:27017')
    mongo = client[document]
    await init_beanie(database=mongo, document_models=models)

    # Initialize ranks in the db if it doesn't exist
    existing_ranks = await Rank.all().to_list()
    if not existing_ranks:
        for name in RANKS:
            rank = Rank(name=name)
            await rank.save()
    
    # Initialize permissions in the db if it doesn't exist
    existing_permissions = await Permission.all().to_list()
    guild_master = await Rank.find_one(Rank.name == 'Guild Master')
    if not existing_permissions:
        for p in PERMISSIONS:
            permission = Permission(name=p)
            p_id = await Permission.insert_one(permission)
            p_id = p_id._id
            
            # Assign all permissions to guild master
            rp = RankPermission(rank_id=guild_master._id, permission_id=p_id)
            await rp.save()
    
    # Create a sample user, this should not exist in the codebase at all but only for testing purposes
    await User.all().delete()
    await Player.all().delete()
    existing_user = await User.all().to_list()
    if not existing_user:
        password = get_password_hash('pass')
        u = await User.insert_one(User(username='user', password=password))
        # Create a player/character associated with the user
        p = Player(user_id=str(u.id))
        await p.save()