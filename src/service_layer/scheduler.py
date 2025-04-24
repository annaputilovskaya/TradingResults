import logging
from datetime import datetime
from time import time

from aiohttp import ClientSession
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from fastapi_cache import FastAPICache

from src import dbh
from src.service_layer.parser.data_parser import parse_trading_results
from src.service_layer.parser.links_parser import get_new_trading_results_links
from src.service_layer.queries import get_dates

log = logging.getLogger(__name__)


async def main_parser():
    """
    Main function to parse and save trading results.
    """
    async with dbh.session_factory() as db:
        result = await get_dates(db=db, days=1)
        if result:
            earliest_date = result[0]
        else:
            earliest_date = "20221231"
        log.info(f"Earliest date: {earliest_date}.")
    t0 = time()
    async with ClientSession() as session:
        links = await get_new_trading_results_links(session, earliest_date)
    if links:
        await parse_trading_results(links)
        log.info(f"Finished. Execution time {time() - t0:.3f} second")
    else:
        log.info("No new trading results found.")


async def cache_clear():
    """
    Clear redis cache.
    """
    try:
        await FastAPICache.clear()
        log.info("Cache cleared")
    except Exception as e:
        log.error(f"Error cleaning cache: {e}.")


def add_jobs_to_scheduler(scheduler):
    """
    Add jobs to parse data and to clean cache to scheduler.
    """

    first_runtime = datetime.now()
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
    return scheduler
