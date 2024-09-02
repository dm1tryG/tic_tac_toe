from enum import Enum

import httpx
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from game.model import Game, Database


class Player(str, Enum):
    CROSS = "x"
    NOUGHT = "o"


class GameService:
    def __init__(self):
        self.engine = Database().engine
        self.board = []
        # TODO: add to settings (Pydantic Settings with envs for example)
        self.random_api_url = "http://random_api:5000/random/default/choice"

    async def create_game(self, game: Game) -> Game:
        # TODO: Create session generator in Database
        async with AsyncSession(self.engine) as session:
            async with session.begin():
                session.add(game)
            await session.commit()
            await session.refresh(game)
            return game

    async def get_games(self):
        async with AsyncSession(self.engine) as session:
            result = await session.execute(select(Game))
            games = result.scalars().all()
            return games

    async def get_game_preview(self, game_id: int) -> str:
        async with AsyncSession(self.engine) as session:
            result = await session.execute(
                select(Game).where(Game.id == game_id)
            )
            game = result.scalars().first()
            if game is None:
                raise HTTPException(status_code=404, detail="Game not found")
        return game.board

    async def simulate(self, title: str) -> Game:
        # TODO: move board_width to settings
        board_width = 3

        board = [' '] * board_width**2
        board_index = list(range(board_width**2))
        current_player = Player.CROSS
        while True:
            move = await self.get_random_step(board_index)
            board_index.remove(move)
            board[move] = current_player
            winner = GameService.check_winner(board)
            if winner or ' ' not in board:
                break
            current_player = Player.NOUGHT if current_player == Player.CROSS else Player.CROSS

        return await self.create_game(
            game=Game(
                title=title,
                board=GameService.board_to_text(board),
                winner=winner,
            )
        )

    async def get_random_step(self, empty_cells: list) -> int:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=self.random_api_url,
                params={
                    "value": empty_cells
                }
            )
            return int(response.json()["value"])

    @staticmethod
    def check_winner(board):
        combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for combo in combinations:
            if board[combo[0]] != ' ' and board[combo[0]] == board[combo[1]] == board[combo[2]]:
                return board[combo[0]]
        return None

    @staticmethod
    def board_to_text(board):
        # TODO: move board_width to settings or method args (its copy in simulate())
        size = 3
        return '\n'.join(
            ' '.join(board[i * size:(i + 1) * size])
            for i in range(size)
        )
