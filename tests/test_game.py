from unittest.mock import patch, AsyncMock

import pytest

from game.service import GameService, Player


@pytest.mark.asyncio
async def test_create_game(client):
    response = await client.post("/games/simulate", json={"title": "Just game"})
    assert response.status_code == 200
    content = response.json()
    assert "title" in content
    assert content["title"] == "Just game"
    assert "board" in content
    assert "winner" in content
    assert content["id"] is not None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "random_moves,expected_winner",
    [
        ([1, 0, 2, 4, 3, 5, 7, 6, 8], None),
        ([0, 3, 1, 4, 2], Player.CROSS),
        ([5, 0, 6, 1, 7, 2], Player.NOUGHT),
    ]
)
async def test_simulation_with_winner_x(client, random_moves, expected_winner):
    game_service = GameService()
    with patch.object(game_service, 'get_random_step', new_callable=AsyncMock) as mock_get_random_step, \
            patch.object(game_service, 'check_winner', return_value=None) as mock_check_winner:

        mock_check_winner.return_value = expected_winner
        mock_get_random_step.side_effect = random_moves

        game = await game_service.simulate(title="Test Game")
        assert mock_get_random_step.call_count == len(random_moves)
        assert game.winner == expected_winner


@pytest.mark.asyncio
async def test_preview(client):
    response = await client.post("/games/simulate", json={"title": "Just game"})
    assert response.status_code == 200
    content = response.json()
    response = await client.get(f"/games/{content['id']}/preview")
    assert response.status_code == 200
    content = response.text
    assert len(content.split("\n")) == 3
