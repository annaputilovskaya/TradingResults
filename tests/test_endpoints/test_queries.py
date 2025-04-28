from datetime import date

import pytest

from src.service_layer.queries import get_dates, get_filtered_trading_results, get_last_results


@pytest.mark.asyncio
class TestQueries:

    @pytest.mark.parametrize(
        "days, dates",
        [
            (2, ["20250101", "20240101"]),
            (10, ["20250101", "20240101", "20230103", "20230102", "20230101"]),
            ]
    )
    async def test_get_dates(self, days, dates, get_async_session):
        assert await get_dates(get_async_session, days) == dates

    @pytest.mark.parametrize(
        "filters, start_date, end_date, amount",
        [
            (
                    {
                        "oil_id": "A100",
                        "delivery_type_id": "F",
                    },
                    date(2023, 1, 3),
                    None,
                    9,

            ),
            (
                    {
                        "oil_id": "A100",
                        "delivery_type_id": "A",
                        "delivery_basis_id": "ABS"
                    },
                    None,
                    date(2024, 4, 3),
                    4
            ),
            (
                    {
                        "oil_id": "A200",
                        "delivery_type_id": "A",
                        "delivery_basis_id": "ABS"
                    },
                    None,
                    None,
                    0
            )
        ]
    )
    async def test_get_filtered_trading_results(self, filters, start_date, end_date, amount, get_async_session):
        db_results = await get_filtered_trading_results(get_async_session, filters, start_date, end_date)
        assert len(db_results) == amount

    @pytest.mark.parametrize(
        "filters, amount",
        [
            (
                    {
                        "oil_id": "A100",
                        "delivery_type_id": "A",
                    },
                    2,

            ),
            (
                    {},
                    5
            ),
            (
                    {
                        "oil_id": "A200",
                        "delivery_type_id": "A",
                        "delivery_basis_id": "ABS"
                    },
                    0
            )
        ]
    )
    async def test_get_last_results(self, filters, amount, get_async_session):
        data = await get_last_results(get_async_session, filters)
        assert len(data) == amount
