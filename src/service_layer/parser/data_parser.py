import logging
from io import BytesIO

import numpy
import pandas as pd
from aiohttp import ClientSession

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
