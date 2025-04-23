import logging

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from src.service_layer.utils import get_date_from_link

log = logging.getLogger(__name__)


async def get_html(url: str, session: ClientSession) -> str | None:
    """
    Sends a GET request to the given URL and returns the response data.

    Args:
        url (str): The URL to fetch data from.
        session (ClientSession): The aiohttp ClientSession object.

    Returns:
        str | None: The response data as a string or None if an error occurred.
    """
    try:
        async with session.get(url) as response:
            data = await response.text()
            return data
    except Exception as e:
        log.error(f"Error: Failed to fetch data from {url}: {e}")
        raise e


def extract_links_from_response(
    response: str, earliest_date: str, links: set[str], is_new: bool
) -> tuple[set[str], bool]:
    """
    Extracts links to XLS files with daily trading results from the given HTML response.

    Args:
        response (str): The HTML response containing the trading results.
        earliest_date (str): The earliest date to consider in the format "YYYYMMDD".
        links (set[str]): The set of links to add new ones to.
        is_new (bool): A boolean indicating if new links were found.

    Returns:
        tuple[set[str], bool]: The updated set of links and a boolean indicating if new links were found.
    """
    soup = BeautifulSoup(response, "html.parser")
    block = soup.find("div", class_="accordeon-inner")
    items = block.select(
        "div.accordeon-inner__wrap-item",
    )
    for item in items:
        string = item.find("a")
        link = string.get("href")
        if link:
            date = get_date_from_link(link)
            if date >= earliest_date:
                links.add(link)
            else:
                is_new = False
                break
    return links, is_new
