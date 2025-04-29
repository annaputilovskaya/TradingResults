import asyncio
import pytest
import pytest_asyncio

from typing import Any, AsyncGenerator
from contextlib import asynccontextmanager
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from httpx import ASGITransport, AsyncClient
from sqlalchemy import insert

from src.config import settings
from src.models import test_dbh, Base, ORMTradingResult
from src.models.domain import TradingResult
from src.routers import router

test_db = test_dbh(
    settings.db.test_url,
)

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

async def override_get_async_session():
    """
    Overrides dependency for getting asynchronous session for testing.

    Yields:
        AsyncSession: Asynchronous session for testing.
    """
    async with test_db.session_factory() as session:
        yield session


@pytest.fixture(scope='package', autouse=True)
def event_loop():
    """
    Yields event loop for test session.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='package', autouse=True)
async def app() -> AsyncGenerator[LifespanManager, Any]:
    """
    Create FastAPI application for testing.

    Yields:
         FastAPI application.
    """
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        """
        Prepare testing database for tests.
        """
        FastAPICache.init(InMemoryBackend())
        async with test_db.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            await conn.execute(insert(ORMTradingResult), test_data)
            await conn.commit()
        yield
        async with test_db.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        FastAPICache.reset()


    test_app = FastAPI(docs_url=None,
                  redoc_url=None,
                  lifespan=lifespan,
                  )
    test_app.include_router(router=router)
    test_app.dependency_overrides[test_db.session_getter] = override_get_async_session

    async with LifespanManager(test_app) as manager:
        yield manager.app


@pytest_asyncio.fixture(scope="package", autouse=True)
async def get_async_session():
    """
    Overrides dependency for getting asynchronous session for testing.

    Yields:
        AsyncSession: Asynchronous session for testing.
    """
    async with test_db.session_factory() as session:
        yield session


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
    return await FastAPICache.clear()
