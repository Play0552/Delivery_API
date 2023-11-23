from datetime import timedelta
from typing import Optional
from pydantic import BaseModel


class CourierRegister(BaseModel):
    name: str
    districts: list[str]


class CouriersInfo(BaseModel):
    id: int
    name: str


class CourierInfo(BaseModel):
    id: int
    name: str
    active_order: Optional[dict] = None
    avg_order_complete_time: Optional[timedelta] = None
    avg_day_orders: Optional[float] = None

