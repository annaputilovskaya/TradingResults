import logging
from io import BytesIO
from time import time

import asyncio
import numpy
import pandas as pd
from aiohttp import ClientSession

from src import dbh
from src.config import HOST
from src.service_layer.parser.results_generator import generate_trading_result_objects

log = logging.getLogger(__name__)


async def get_bytes(url: str, session: ClientSession) -> bytes | None:
    """
    Sends a GET async request to the given URL and returns the response bytes.

    Args:
        url (str): The URL to send the GET request to.
        session (ClientSession): The aiohttp ClientSession to use for the request.

    Returns:
        bytes: The response bytes from the GET request or None if an error occurred.
    """
    try:
        async with session.get(url) as response:
            data = await response.read()
            return data
    except Exception as e:
        log.error(f"Error: Failed to fetch data from {url}: {e}")
        raise e


def extract_data_from_file(data: bytes) -> pd.DataFrame | None:
    """
    Reads data from an XLS file and filter it based on certain conditions.

    Args:
        data (bytes): The XLS file data to read.

    Returns:
        pd.DataFrame: The filtered DataFrame or None if an error occurred.
    """
    file = pd.read_excel(BytesIO(data), index_col=False)
    rows, cols = numpy.where(file == "Единица измерения: Метрическая тонна")
    row = rows[0] + 2

    filtered = pd.read_excel(
        io=data,
        skiprows=row,
        usecols=[1, 2, 3, 4, 5, 14],
    )
    return filtered[filtered["Количество\nДоговоров,\nшт."] != "-"]


async def get_data_by_link(link: str) -> pd.DataFrame | None:
    """
    Sends a GET request to the given URL, extracts data from the XLS file.

    Args:
        link (str): The URL to send the GET request to.

    Returns:
        pd.DataFrame: The filtered DataFrame or None if an error occurred.
        str: The link from which the data was fetched.
    """
    t0 = time()
    async with ClientSession() as session:
        filepath = HOST + link
        log.info(f"Started reading {filepath}")
        data = await get_bytes(filepath, session)
        try:
            df = await asyncio.to_thread(extract_data_from_file, data=data)
        except Exception as e:
            log.error(f"Error extracting data from {filepath}: {e}")
        else:
            log.info(f"Finished reading. Execution time {time() - t0:.3f} seconds.")
            return df, link


async def write_to_db(results_list: list) -> None:
    """
    Save the given trading results to the database.

    Args:
        results_list (list): The list of TradingResult objects to save to the database.
    """
    t0 = time()
    log.info(f"Start writing results to db.")
    async with dbh.session_factory() as session:
        session.add_all(results_list)
        try:
            log.info(
                f"Finished writing results to db. Execution time {time() - t0:.3f} seconds."
            )
            await session.commit()
        except Exception as e:
            log.error(f"Error saving trading results: {e} to db.")
            await session.rollback()
