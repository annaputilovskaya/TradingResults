import logging
from contextlib import asynccontextmanager
from datetime import datetime

import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from src import dbh
from src.config import settings
from src.service_layer.scheduler import main_parser, cache_clear

log = logging.getLogger(__name__)

logging.basicConfig(
    level=settings.logging.log_level_value,
    format=settings.logging.log_format,
    filename="logs/async_app.log",
)

scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    redis = aioredis.from_url(
        settings.redis.redis_url, encoding="utf-8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    first_runtime = datetime.now()
    try:

        scheduler.add_job(
            func=main_parser,
            trigger=DateTrigger(run_date=first_runtime),
            id="add_first_trading_results_job",
            replace_existing=True,
        ),
        scheduler.add_job(
            func=main_parser,
            trigger=CronTrigger(hour=14, minute=1, timezone="Europe/Moscow"),
            id="add_trading_results_job",
            replace_existing=True,
        )
        scheduler.add_job(
            func=cache_clear,
            trigger=CronTrigger(hour=14, minute=11, timezone="Europe/Moscow"),
            id="clear_redis_cache",
            replace_existing=True,
        )
        scheduler.start()
        log.warning("Start scheduler.")
        yield
    except Exception as e:
        log.error(f"Error initializing scheduler: {e}.")
    # shutdown
    finally:
        scheduler.shutdown()
        log.warning("Stop scheduler.")
        await dbh.dispose()


main_app = FastAPI(title="SpimexTradingResults", lifespan=lifespan)


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app", host=settings.run.host, port=settings.run.port, reload=True
    )
