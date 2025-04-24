import re
from datetime import date

from fastapi import HTTPException


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


def validate_dates_interval(
    start_date: date,
    end_date: date,
) -> tuple[str | date, str]:
    """
    Validate start and end dates.

    Args:
        start_date (date | None): Beginning of the period for analysis of dynamics.
        end_date (date | None): End of the period for analysis of dynamics.

    Returns:
        start_date (date | None): Validated beginning of the period for analysis of dynamics.
        end_date (date | None): Validated end of the period for analysis of dynamics.
    """
    if start_date:
        start_date = start_date.strftime("%Y%m%d")
    if not start_date or start_date < "20230101":
        start_date = "20230101"
    if end_date:
        end_date = end_date.strftime("%Y%m%d")
    else:
        end_date = date.today().strftime("%Y%m%d")
    if start_date > end_date:
        raise HTTPException(
            status_code=400, detail="Start date should be less or equal to end date"
        )
    return start_date, end_date
