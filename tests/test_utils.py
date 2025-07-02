from datetime import date
from contextlib import nullcontext as does_not_raise

import pytest
from fastapi import HTTPException

from src.service_layer.utils import (
    validate_dates_interval,
    set_filters,
    get_date_from_link,
)


@pytest.mark.parametrize(
    "start_date, end_date, expected_start_date, expected_end_date, expectation",
    [
        (None, None, "20230101", date.today().strftime("%Y%m%d"), does_not_raise()),
        (date(2022, 1, 1), date(2025, 2, 1), "20230101", "20250201", does_not_raise()),
        (date(2024, 1, 1), date(2026, 1, 1), "20240101", "20260101", does_not_raise()),
        (
            date(2025, 2, 1),
            date(2022, 1, 1),
            "20250201",
            "20220101",
            pytest.raises(HTTPException),
        ),
        (
            "20230101",
            date(2026, 1, 1),
            "20230101",
            "20260101",
            pytest.raises(AttributeError),
        ),
        (
            20230101,
            date(2026, 1, 1),
            "20230101",
            "20260101",
            pytest.raises(AttributeError),
        ),
    ],
)
def test_validate_dates_interval(
    start_date, end_date, expected_start_date, expected_end_date, expectation
):
    with expectation:
        assert validate_dates_interval(start_date, end_date) == (
            expected_start_date,
            expected_end_date,
        )


@pytest.mark.parametrize(
    "oil_id, delivery_type_id, delivery_basis_id, filters",
    [
        (
            "A100",
            "A",
            "ABS",
            {"oil_id": "A100", "delivery_type_id": "A", "delivery_basis_id": "ABS"},
        ),
        (None, "A", "ABS", {"delivery_type_id": "A", "delivery_basis_id": "ABS"}),
        ("A100", None, "ABS", {"oil_id": "A100", "delivery_basis_id": "ABS"}),
        (
            "A100",
            "A",
            None,
            {
                "oil_id": "A100",
                "delivery_type_id": "A",
            },
        ),
        (None, None, None, {}),
    ],
)
def test_set_filters(oil_id, delivery_type_id, delivery_basis_id, filters):
    assert set_filters(oil_id, delivery_type_id, delivery_basis_id) == filters


@pytest.mark.parametrize(
    "link, date_str",
    [
        (
            "https://spimex.com/upload/reports/oil_xls/oil_xls_20230119162000.xls?r=5887",
            "20230119",
        ),
        ("https://spimex.com", None),
    ],
)
def test_get_date_from_link(link, date_str):
    assert get_date_from_link(link) == date_str
