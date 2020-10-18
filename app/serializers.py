from pydantic import BaseModel
from typing import List, Dict, Optional, Any


class CartSerializer(BaseModel):
    product: str
    quantity: int




