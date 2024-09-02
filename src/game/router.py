from fastapi import APIRouter
from starlette.responses import PlainTextResponse

from game.schema import CreateGameSchema
from game.service import GameService

router = APIRouter(prefix="/games")


@router.get("/{game_id}/preview")
async def get_game_preview(game_id: int):
    """
    Get game preview in plain text
    """
    service = GameService()
    preview = await service.get_game_preview(game_id=game_id)
    return PlainTextResponse(preview, media_type="text/plain")


@router.post("/simulate")
async def simulate_game(
    payload: CreateGameSchema
):
    """
    Simulate game
    """
    service = GameService()
    return await service.simulate(
        title=payload.title
    )
