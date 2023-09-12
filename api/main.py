from fastapi import FastAPI

from .auth.models import User
from .auth.router import auth_router
from .database import init_db
from .guild.models import Guild, GuildApplication, GuildInvite
from .guild.router import guild_router
from .player.models import Permission, Player, Rank, RankPermission

app = FastAPI()

@app.on_event('startup')
async def startup():
    # This will initialize the documents if they don't exist yet
    await init_db(
        document='mmorpg',
        models=[
            Guild,
            GuildApplication,
            GuildInvite,
            Player,
            Rank,
            RankPermission,
            Permission,
            User
        ]
    )

app.include_router(guild_router)
app.include_router(auth_router)

@app.get("/health", summary="Check that the service is operational")
def health():
    """
    Sanity check - this will let the user know that the service is operational.
    It is also used as part of the HEALTHCHECK. Docker uses curl to check that the API service is still running, by exercising this endpoint.
    """
    return {"status": "OK"}
