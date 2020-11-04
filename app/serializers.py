from pydantic import BaseModel


class CartSerializer(BaseModel):
    product: str
    quantity: int




