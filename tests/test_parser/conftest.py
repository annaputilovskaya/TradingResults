from io import BytesIO

import pandas as pd
import pytest


@pytest.fixture()
def dataframe1():
    data = {
        "Unnamed: 0": [
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ],
        "Форма СЭТ-БТ": [
            "A592AASK01O",
            "Единица измерения: Метрическая тонна",
            "Код\nИнструмента",
            None,
            "A100STI060F",
            "Итого:",
            "Итого по секции:",
        ],
        "Unnamed: 2": [
            "Some",
            None,
            "Наименование\nИнструмента",
            None,
            "Some",
            None,
            None,
        ],
        "Unnamed: 3": ["Some", None, "Базис\nпоставки", None, "Some", None, None],
        "Unnamed: 4": [
            "-",
            None,
            "Объем\nДоговоров\nв единицах\nизмерения",
            None,
            "120",
            None,
            None,
        ],
        "Unnamed: 5": [
            "-",
            None,
            "Обьем\nДоговоров,\nруб.",
            None,
            "8400000",
            None,
            None,
        ],
        "Unnamed: 6": ["-", "-", "-", "-", "-", "-", "-"],
        "Unnamed: 7": ["-", "-", "-", "-", "-", "-", "-"],
        "Unnamed: 8": ["-", "-", "-", "-", "-", "-", "-"],
        "Unnamed: 9": ["-", "-", "-", "-", "-", "-", "-"],
        "Unnamed: 10": ["-", "-", "-", "-", "-", "-", "-"],
        "Unnamed: 11": ["-", "-", "-", "-", "-", "-", "-"],
        "Unnamed: 12": ["-", "-", "-", "-", "-", "-", "-"],
        "Unnamed: 13": ["-", "-", "-", "-", "-", "-", "-"],
        "Unnamed: 14": [
            "-",
            None,
            "Количество\nДоговоров,\nшт.",
            None,
            "5",
            "1000",
            "1000",
        ],
    }
    return pd.DataFrame(data)


@pytest.fixture()
def excel_data(dataframe1) -> BytesIO:
    output = BytesIO()
    dataframe1.to_excel(output, index=False)
    output.seek(0)
    return output


@pytest.fixture()
def dataframe2():
    data = {
        "Код\nИнструмента": [None, "A100STI060F", "Итого:", "Итого по секции:"],
        "Наименование\nИнструмента": [None, "Some", None, None],
        "Базис\nпоставки": [None, "Some", None, None],
        "Объем\nДоговоров\nв единицах\nизмерения": [None, 120.0, None, None],
        "Обьем\nДоговоров,\nруб.": [None, 8400000.0, None, None],
        "Количество\nДоговоров,\nшт.": [None, 5.0, 1000.0, 1000.0],
    }
    return pd.DataFrame(data)
