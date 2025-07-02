from datetime import datetime


class TradingResult:
    """
    Trading result.

    Attributes:
        exchange_product_id (str): The exchange product ID.
        exchange_product_name (str): The exchange product name.
        oil_id (str): The oil ID.
        delivery_basis_id (str): The delivery basis ID.
        delivery_basis_name (str): The delivery basis name.
        delivery_type_id (str): The delivery type ID.
        volume (int): The volume of contracts in tones.
        total (int): The total value of contracts in rubles.
        count (int): The count of contracts.
        date (str): The date of trading.
        created_on (datetime): The date and time when the result was created.
        updated_on (datetime): The date and time when the result was updated.
    """

    def __init__(
        self,
        exchange_product_id: str,
        exchange_product_name: str,
        delivery_basis_name: str,
        volume: int,
        total: int,
        count: int,
        date: str,
    ):
        """
        Initializes the instance based on trading data

        Args:
            exchange_product_id (str): The exchange product ID.
            exchange_product_name (str): The exchange product name.
            delivery_basis_name (str): The delivery basis name.
            volume (int): The volume of contracts in tones.
            total (int): The total value of contracts in rubles.
            count (int): The count of contracts.
            date (str): The date of trading.
        """
        self.exchange_product_id = exchange_product_id
        self.exchange_product_name = exchange_product_name
        self.oil_id = exchange_product_id[:4]
        self.delivery_basis_id = exchange_product_id[4:7]
        self.delivery_basis_name = delivery_basis_name
        self.delivery_type_id = exchange_product_id[-1]
        self.volume = volume
        self.total = total
        self.count = count
        self.date = date
        self.created_on = datetime.now()
        self.updated_on = datetime.now()

    def to_dict(self):
        """
        Converts trading result attributes to a dictionary.

        Returns:
            The attributes of trading result as a dictionary.
        """
        return {
            "exchange_product_id": self.exchange_product_id,
            "exchange_product_name": self.exchange_product_name,
            "oil_id": self.oil_id,
            "delivery_basis_id": self.delivery_basis_id,
            "delivery_basis_name": self.delivery_basis_name,
            "delivery_type_id": self.delivery_type_id,
            "volume": self.volume,
            "total": self.total,
            "count": self.count,
            "date": self.date,
            "created_on": self.created_on,
            "updated_on": self.updated_on if self.updated_on else None,
        }
