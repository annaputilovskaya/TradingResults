import pandas as pd

from src.models import ORMTradingResult
from src.models.domain import TradingResult
from src.service_layer.utils import get_date_from_link


def generate_trading_result_objects(data: pd.DataFrame, link: str):
    """
    Generates trading results objects from rows of DataFrame.

    Args:
        data (pd.DataFrame): DataFrame containing trading result data.
        link (str): Link to the source data.

    Yields:
        ORMTradingResult: Trading result object in database.
    """
    for i in range(1, len(data) - 2):
        row = data.iloc[i]
        if (
            pd.isna(row["Объем\nДоговоров\nв единицах\nизмерения"])
            or row.apply(lambda x: "Итого" in str(x)).any()
        ):
            continue
        else:
            yield ORMTradingResult(
                **TradingResult(
                    exchange_product_id=row["Код\nИнструмента"],
                    exchange_product_name=row["Наименование\nИнструмента"],
                    delivery_basis_name=row["Базис\nпоставки"],
                    volume=int(row["Объем\nДоговоров\nв единицах\nизмерения"]),
                    total=int(row["Обьем\nДоговоров,\nруб."]),
                    count=int(row["Количество\nДоговоров,\nшт."]),
                    date=get_date_from_link(link),
                ).to_dict()
            )
