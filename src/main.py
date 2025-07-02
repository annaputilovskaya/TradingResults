import logging
import os.path
from contextlib import asynccontextmanager

import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from src.config import settings, LOG_DIR
from src.models import dbh
from src.routers import router
from src.service_layer.scheduler import add_jobs_to_scheduler

log = logging.getLogger(__name__)

logging.basicConfig(
    level=settings.logging.log_level_value,
    format=settings.logging.log_format,
    filename=os.path.join(LOG_DIR, "async_app.log"),
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    redis = aioredis.from_url(
        settings.redis.redis_url, encoding="utf-8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    scheduler = AsyncIOScheduler()
    try:
        scheduler = add_jobs_to_scheduler(scheduler)
        yield
    except Exception as e:
        log.error(f"Error initializing scheduler: {e}.")
    # shutdown
    finally:
        scheduler.shutdown()
        log.warning("Stop scheduler.")
        await dbh.dispose()


main_app = FastAPI(title="SpimexTradingResults", lifespan=lifespan)
main_app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app", host=settings.run.host, port=settings.run.port, reload=True
    )
