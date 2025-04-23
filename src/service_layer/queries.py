from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src import ORMTradingResult


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
