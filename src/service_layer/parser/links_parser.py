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
