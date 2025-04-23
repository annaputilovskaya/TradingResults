import asyncio
import logging
from time import time

from aiohttp import ClientSession

from src.service_layer.parser.data_parser import parse_trading_results
from src.service_layer.parser.links_parser import get_new_trading_results_links


log = logging.getLogger(__name__)


async def main_parser():
    """
    Main function to parse and save trading results.
    """
    t0 = time()
    async with ClientSession() as session:
        links = await get_new_trading_results_links(session)
    if links:
        await parse_trading_results(links)
        log.info(f"Finished. Execution time {time() - t0:.3f} second")
    else:
        log.info("No new trading results found.")


if __name__ == "__main__":
    asyncio.run(main_parser())