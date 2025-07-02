from datetime import date
from unittest.mock import AsyncMock

import pytest

from src.service_layer.queries import (
    get_dates,
    get_filtered_trading_results,
    get_last_results,
)
from src.service_layer.utils import set_filters


@pytest.mark.asyncio
@pytest.mark.usefixtures("disable_cache")
class TestAPI:

    @pytest.mark.parametrize(
        "days, dates",
        [
            (2, ["20250101", "20240101"]),
            (10, ["20250101", "20240101", "20230103", "20230102", "20230101"]),
        ],
    )
    async def test_get_last_trading_dates(
        self, days, dates, client, get_async_session, monkeypatch
    ):

        mock_get_dates = AsyncMock(
            return_value=await get_dates(get_async_session, days)
        )
        monkeypatch.setattr("src.routers.get_dates", mock_get_dates)
        response = await client.get(f"/dates?days={days}")
        assert response.status_code == 200
        assert response.json() == dates

    @pytest.mark.parametrize(
        "oil_id, delivery_type_id, delivery_basis_id, start_date, end_date, results",
        [
            (
                None,
                "F",
                "ANK",
                date(2025, 1, 1),
                None,
                [
                    dict(
                        exchange_product_id="A100ANK060F",
                        exchange_product_name="Product",
                        delivery_basis_name="Basis",
                        volume=10,
                        total=100000,
                        count=1,
                        date="20250101",
                        oil_id="A100",
                        delivery_basis_id="ANK",
                        delivery_type_id="F",
                    )
                ],
            ),
            (
                "A100",
                "A",
                "ABS",
                None,
                date(2023, 1, 2),
                [
                    dict(
                        exchange_product_id="A100ABS025A",
                        exchange_product_name="Product",
                        delivery_basis_name="Basis",
                        volume=10,
                        total=100000,
                        count=1,
                        date="20230102",
                        oil_id="A100",
                        delivery_basis_id="ABS",
                        delivery_type_id="A",
                    ),
                    dict(
                        exchange_product_id="A100ABS025A",
                        exchange_product_name="Product",
                        delivery_basis_name="Basis",
                        volume=10,
                        total=100000,
                        count=1,
                        date="20230101",
                        oil_id="A100",
                        delivery_basis_id="ABS",
                        delivery_type_id="A",
                    ),
                ],
            ),
            (
                "A200",
                "A",
                "ABS",
                None,
                None,
                {"detail": "Trading results for given parameters not found"},
            ),
        ],
    )
    async def test_get_dynamics(
        self,
        oil_id,
        delivery_type_id,
        delivery_basis_id,
        start_date,
        end_date,
        results,
        client,
        get_async_session,
        monkeypatch,
    ):
        filters = set_filters(oil_id, delivery_type_id, delivery_basis_id)
        mock_get_filtered_trading_results = AsyncMock(
            return_value=await get_filtered_trading_results(
                get_async_session, filters, start_date, end_date
            )
        )
        monkeypatch.setattr(
            "src.routers.get_filtered_trading_results",
            mock_get_filtered_trading_results,
        )
        response = await client.get(
            f"/?oil_id={oil_id}, delivery_type_id={delivery_type_id}, delivery_basis_id={delivery_basis_id}, start_date={start_date}, end_date={end_date}"
        )
        assert response.json() == results

    @pytest.mark.parametrize(
        "oil_id, delivery_type_id, delivery_basis_id, results",
        [
            (
                None,
                "F",
                "ANK",
                [
                    dict(
                        exchange_product_id="A100ANK060F",
                        exchange_product_name="Product",
                        delivery_basis_name="Basis",
                        volume=10,
                        total=100000,
                        count=1,
                        date="20250101",
                        oil_id="A100",
                        delivery_basis_id="ANK",
                        delivery_type_id="F",
                    )
                ],
            ),
            (
                None,
                "A",
                None,
                [
                    dict(
                        exchange_product_id="A100ABS025A",
                        exchange_product_name="Product",
                        delivery_basis_name="Basis",
                        volume=10,
                        total=100000,
                        count=1,
                        date="20250101",
                        oil_id="A100",
                        delivery_basis_id="ABS",
                        delivery_type_id="A",
                    ),
                    dict(
                        exchange_product_id="A100NFT005A",
                        exchange_product_name="Product",
                        delivery_basis_name="Basis",
                        volume=10,
                        total=100000,
                        count=1,
                        date="20250101",
                        oil_id="A100",
                        delivery_basis_id="NFT",
                        delivery_type_id="A",
                    ),
                ],
            ),
        ],
    )
    async def test_get_trading_results(
        self,
        oil_id,
        delivery_type_id,
        delivery_basis_id,
        results,
        client,
        get_async_session,
        monkeypatch,
    ):
        filters = set_filters(oil_id, delivery_type_id, delivery_basis_id)
        mock_get_filtered_trading_results = AsyncMock(
            return_value=await get_last_results(get_async_session, filters)
        )
        monkeypatch.setattr(
            "src.routers.get_last_results", mock_get_filtered_trading_results
        )
        response = await client.get(
            f"/last?oil_id={oil_id}, delivery_type_id={delivery_type_id}, delivery_basis_id={delivery_basis_id}"
        )
        assert response.json() == results
