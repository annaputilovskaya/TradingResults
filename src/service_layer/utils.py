import re


def get_date_from_link(link: str) -> str:
    """
    Extracts date from the link.

    Args:
        link (str): The URL of the page containing the trading results.

    Returns:
        str: The date extracted from the link in the format "YYYYMMDD".
    """
    match = re.search(r"oil_xls_(\d{8})\d{6}", link)
    return match.group(1)