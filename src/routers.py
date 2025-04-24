from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from src import dbh
from src.service_layer.queries import get_dates, get_filtered_trading_results
from src.service_layer.utils import set_filters

router = APIRouter(tags=["TradingResults"])


@router.get("/dates")
@cache()
async def get_last_trading_dates(
    db: Annotated[AsyncSession, Depends(dbh.session_getter)],
    days: int,
):
    return await get_dates(db=db, days=days)


@router.get(
    "/",
    summary="The list of trading results matching the given parameters for a certain period",
)
@cache()
async def get_dynamics(
        db: Annotated[AsyncSession, Depends(dbh.session_getter)],
        oil_id: str | None = None,
        delivery_type_id: str| None = None,
        delivery_basis_id: str| None = None,
        start_date: date | None = None,
        end_date: date | None = None,
):
    filters = set_filters(oil_id, delivery_type_id, delivery_basis_id)
    results = await get_filtered_trading_results(
        db=db, filters=filters, start_date=start_date, end_date=end_date
    )
    if not results:
        raise HTTPException(
            status_code=404,
            detail=f"Trading results for given parameters not found",
        )
    return
