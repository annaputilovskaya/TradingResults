from datetime import date

from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import ORMTradingResult
from src.service_layer.utils import validate_dates_interval


async def get_dates(
    db: AsyncSession,
    days: int,
) -> list[str]:
    """
    Gets a list of dates of the last trading days.

    Args:
        db (AsyncSession): Asynchronous session with the database.
        days (int): Number of last trading days.

    Returns:
        list[str]: List of dates of the last trading days in the format "YYYYMMDD".
    """
    dates = await db.scalars(
        select(ORMTradingResult.date)
        .order_by(ORMTradingResult.date.desc())
        .distinct()
        .limit(days)
    )
    return list(dates.all())


async def get_filtered_trading_results(
    db: AsyncSession,
    filters: dict[str, str] | None,
    start_date: date | None = None,
    end_date: date | None = None,
) -> list[ORMTradingResult]:
    """
    Gets a list of trading results for a given period.

    Args:
        db (AsyncSession): Asynchronous session with the database.
        filters (dict[str, str] | None): Optional filters for trading results parameters.
        start_date (date | None): Beginning of the period for analysis of dynamics.
        end_date (date | None): End of the period for analysis of dynamics.

    Returns:
        list(ORMTradingResult): List of trading results for a given period.
    """
    start_date, end_date = validate_dates_interval(start_date, end_date)
    results = await db.scalars(
        select(ORMTradingResult)
        .filter_by(**filters)
        .filter(
            and_(ORMTradingResult.date >= start_date, ORMTradingResult.date <= end_date)
        )
        .order_by(ORMTradingResult.date.desc())
    )
    return list(results.all())


async def get_last_results(
    db: AsyncSession,
    filters: dict[str, str] | None,
) -> list[ORMTradingResult]:
    """
    Gets a list of trading results for the latest date.

    Args:
        db (AsyncSession): Asynchronous session with the database.
        filters (dict[str, str] | None): Optional filters for trading results parameters.

    Returns:
        list(ORMTradingResult): List of trading results for the latest date.
    """
    last_date_subquery = (
        select(func.max(ORMTradingResult.date)).select_from(ORMTradingResult)
    )
    query = (
        select(ORMTradingResult)
        .filter_by(**filters).where(ORMTradingResult.date == last_date_subquery)
    )

    results = await db.scalars(query)
    return  list(results.all())
