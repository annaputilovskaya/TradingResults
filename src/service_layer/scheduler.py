import logging
from time import time

from aiohttp import ClientSession
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
            earliest_date = "20230101"
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
