import pandas as pd

from src.service_layer.parser.data_parser import extract_data_from_file


def test_extract_data_from_file(excel_data):
    result = extract_data_from_file(excel_data.read())
    print(result.to_dict("list"))
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 4
    assert result["Количество\nДоговоров,\nшт."].iloc[1] == 5
