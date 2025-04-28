import pytest

from src.service_layer.queries import get_dates


@pytest.mark.usefixtures("app")
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
