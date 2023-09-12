from typing import Annotated

from fastapi import Depends, Request
from fastapi.routing import APIRouter
from loguru import logger

from ..auth.models import User
from ..auth.router import get_current_active_user
from ..models.request import (CreateGuildRequest, GuildApplicationApproval,
                              UpdateGuildMemberRankRequest,
                              UpdateRankPermissionRequest)
from ..player.models import Player, Rank, RankPermission
from .models import Guild, GuildApplication, GuildInvite

guild_router = APIRouter(prefix='/guild')

async def check_member_permission(request: Request) -> None:
    # TODO: Check if player has permissions
    return

@guild_router.get('/list/{guild_id}', tags=['Guild'])
async def get_guild_rosters(guild_id: str):
    members = await Player.find(Player.guild_id == guild_id).to_list()
    return members

@guild_router.post('/create', tags=['Guild'])
async def create_guild(user: Annotated[User, Depends(get_current_active_user)], request: CreateGuildRequest) -> dict:
    response = {
        'success': True
    }
    try:
        guild = await Guild.insert_one(request.guild)
        player = await Player.find_one(Player.user_id == str(user.id))
        player.guild_id = str(guild.id)

        # Assign guild master rank to player
        rank = await Rank.find_one(Rank.name == 'Guild Master')
        player.rank_id = rank.id
        player.save()
        response['data'] = await Guild.get(str(guild.id))
    except Exception as e:
        logger.exception(e)
        response['success'] = False
        response['message'] = 'Failed to create guild. Contact support or try again.'
    return response

@guild_router.post('/invite_player', dependencies=[Depends(check_member_permission)], tags=['Guild'])
async def invite_player(invite: GuildInvite) -> dict:
    # Need to add check if the player is a guild master or has permission
    response = {
        'success': True
    }
    try:
        await invite.save()
    except Exception as e:
        logger.exception(e)
        response['success'] = False
        response['message'] = 'Failed to invite player to guild. Contact support or try again.'
    return response

@guild_router.post('/application/create', tags=['Guild'])
async def apply_to_guild(application: GuildApplication) -> dict:
    response = {
        'success': True
    }
    try:
        # TODO: Verify that the player doesn't belong to any guild
        # but it could also be the case that players are allowed to switch between guilds
        # regardless if they're on a guild or not
        await application.save()
    except Exception as e:
        logger.exception(e)
        response['success'] = False
        response['message'] = 'Failed to apply to guild. Contact support or try again.'
    return response

@guild_router.put(
    '/application/approve/{application_id}',
    dependencies=[Depends(check_member_permission)],
    tags=['Guild'],
)
async def approve_player(application_id: str, approval: GuildApplicationApproval) -> dict:
    response = {
        'success': True
    }
    try:
        application = await GuildApplication.get(application_id)
        application.is_approved = approval.approved
        # This assumes that once approved, the player becomes a member
        # of the guild
        if approval.approved:
            player = await Player.get(application.player_id)
            guild = await Guild.get(application.guild_id)
            player.guild = guild
            player.save()
    except Exception as e:
        logger.exception(e)
        response['success'] = False
        response['message'] = 'Failed to approve application. Contact support or try again.'
    return response

@guild_router.put(
    '/leave/{player_id}',
    tags=['Guild']
)
async def leave_guild(player_id: str) -> dict:
    response = {
        'success': True
    }
    try:
        player = await Player.get(player_id)
        player.guild_id = None
        player.rank_id = None
        player.save()
    except Exception as e:
        logger.exception(e)
        response['success'] = False
        response['message'] = 'Failed to leave guild. Contact support or try again.'
    return response

@guild_router.put(
    '/members/{player_id}/kick',
    dependencies=[Depends(check_member_permission)],
    tags=['Guild'],
)
async def kick_member(player_id: str) -> dict:
    response = {
        'success': True
    }
    try:
        player = await Player.get(player_id)
        player.guild_id = None
        player.rank_id = None
        player.save()
    except Exception as e:
        logger.exception(e)
        response['success'] = False
        response['message'] = 'Failed to leave guild. Contact support or try again.'
    return response

@guild_router.put(
    '/members/rank/update/{player_id}',
    dependencies=[Depends(check_member_permission)],
    tags=['Guild']
)
async def update_member_rank(
    player_id: str,
    request_data: UpdateGuildMemberRankRequest
) -> dict:
    response = {
        'success': True
    }
    try:
        player = await Player.get(player_id)
        player.rank_id = request_data.rank_id
        player.save()
    except Exception as e:
        logger.exception(e)
        response['success'] = False
        response['message'] = 'Failed to update rank. Contact support or try again.'
    return response

@guild_router.put(
    '/rank/permissions/update/{rank_id}',
    dependencies=[Depends(check_member_permission)],
    tags=['Guild']
)
async def update_rank_permissions(
    rank_id: str,
    request_data: UpdateRankPermissionRequest
) -> dict:
    response = {
        'success': True
    }
    try:
        # Delete all permissions related to the rank
        RankPermission.find(
            RankPermission.rank_id == rank_id,
            RankPermission.guild_id == request_data.guild_id
        ).delete()

        # Create permissions from request
        for p in request_data.permission_ids:
            rank_p = RankPermission(
                rank_id=rank_id,
                permission_id=p,
                guild_id=request_data.guild_id
            )
            await rank_p.save()

    except Exception as e:
        logger.exception(e)
        response['success'] = False
        response['message'] = 'Failed to update permissions. Contact support or try again.'
    return response
