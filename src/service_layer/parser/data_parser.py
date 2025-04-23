import logging

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
