from datetime import datetime

from pydantic import BaseModel, Field


class TradingResultSchema(BaseModel):
    exchange_product_id: str = Field(max_length=11)
    exchange_product_name: str
    delivery_basis_name: str
    volume: int
    total: int
    count: int
    date: str = Field(max_length=8)
    oil_id: str = Field(max_length=4)
    delivery_basis_id: str = Field(3)
    delivery_type_id: str = Field(1)
