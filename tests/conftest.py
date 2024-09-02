from httpx import AsyncClient, ASGITransport
import pytest_asyncio

from main import app


@pytest_asyncio.fixture(scope="session")
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
