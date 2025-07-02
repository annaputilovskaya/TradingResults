from sqlalchemy import inspect

from src.service_layer.parser.results_generator import generate_trading_result_objects


def test_generate_trading_result_objects(dataframe2):
    results = list(
        generate_trading_result_objects(dataframe2, "oil_xls_20240212162000.xls?r=2186")
    )
    assert len(results) == 1
    dict_of_attributes = {
        c.key: getattr(results[0], c.key)
        for c in inspect(results[0]).mapper.column_attrs
    }
    dict_of_attributes.pop("created_on")
    dict_of_attributes.pop("updated_on")
    assert dict_of_attributes == {
        "count": 5,
        "date": "20240212",
        "delivery_basis_id": "STI",
        "delivery_basis_name": "Some",
        "delivery_type_id": "F",
        "exchange_product_id": "A100STI060F",
        "exchange_product_name": "Some",
        "id": None,
        "oil_id": "A100",
        "total": 8400000,
        "volume": 120,
    }
