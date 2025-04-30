import pytest
import pytest_asyncio

from typing import Any, AsyncGenerator
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from httpx import ASGITransport, AsyncClient
from sqlalchemy import insert

from src.models import ORMTradingResult
from src.models.domain import TradingResult
from tests.conftest import app, test_db

exchange_product_ids = ["A100ABS025A", "A100ANK060F", "A100NFT005A", "A100NVY060F", "A100STI060F"]
dates = ["20230101", "20230102", "20230103", "20240101", "20250101"]
test_data = [
        TradingResult(
            exchange_product_id=exchange_product_id,
            exchange_product_name="Product",
            delivery_basis_name="Basis",
            volume=10,
            total=100000,
            count=1,
            date=date
        ).to_dict() for exchange_product_id in exchange_product_ids for date in dates
]

@pytest_asyncio.fixture(scope='package', autouse=True)
async def prepare_database():
    """
    Prepare testing database for tests.
    """
    async with test_db.engine.begin() as conn:
        await conn.execute(insert(ORMTradingResult), test_data)
        await conn.commit()
    yield


@pytest_asyncio.fixture(scope='package', autouse=True)
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, Any]:
    """
    Creates asynchronous client for testing.

    Args:
        app(FastAPI): FastAPI application for testing.

    Yields:
         client(AsyncClient): The asynchronous client for testing.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client


@pytest.fixture(name="disable_cache", scope="class")
async def in_memory_cache_clear():
    """
    Disable cache for testing.
    """
    return await FastAPICache.clear()
