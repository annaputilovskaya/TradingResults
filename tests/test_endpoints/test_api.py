from unittest.mock import AsyncMock

import pytest

from src.service_layer.queries import get_dates


@pytest.mark.asyncio
class TestAPI:

    @pytest.mark.usefixtures("disable_cache")
    @pytest.mark.parametrize(
        "days, dates",
        [
            (2, ["20250101", "20240101"]),
            (10, ["20250101", "20240101", "20230103", "20230102", "20230101"]),
            ]
    )
    async def test_get_last_trading_dates(self, days, dates, client, get_async_session, monkeypatch):

        mock_get_dates = AsyncMock(return_value=await get_dates(get_async_session, days))
        monkeypatch.setattr("src.routers.get_dates", mock_get_dates)
        response = await client.get( f"/dates?days={days}")
        assert response.status_code == 200
        assert response.json() == dates
