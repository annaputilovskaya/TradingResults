from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from src import dbh
from src.service_layer.queries import get_dates

router = APIRouter(tags=["TradingResults"])


@router.get("/dates")
@cache()
async def get_last_trading_dates(
    db: Annotated[AsyncSession, Depends(dbh.session_getter)],
    days: int,
):
    return await get_dates(db=db, days=days)
