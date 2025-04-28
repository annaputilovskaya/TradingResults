from datetime import date
from contextlib import  nullcontext as does_not_raise

import pytest
from fastapi import HTTPException

from src.service_layer.utils import validate_dates_interval


@pytest.mark.parametrize(
    "start_date, end_date, expected_start_date, expected_end_date, expectation",
    [
        (None, None, "20230101", date.today().strftime("%Y%m%d"), does_not_raise()),
        (date(2022, 1, 1), date(2025, 2, 1), "20230101", "20250201", does_not_raise()),
        (date(2024,1,1), date(2026,1,1), "20240101", "20260101", does_not_raise()),
        (date(2025, 2, 1), date(2022, 1, 1), "20250201", "20220101", pytest.raises(HTTPException)),
        ("20230101", date(2026,1,1), "20230101", "20260101", pytest.raises(AttributeError)),
        (20230101, date(2026,1,1), "20230101", "20260101", pytest.raises(AttributeError))
    ]
)
def test_validate_dates_interval(start_date, end_date, expected_start_date, expected_end_date, expectation):
    with expectation:
        assert validate_dates_interval(start_date, end_date) == (expected_start_date, expected_end_date)
