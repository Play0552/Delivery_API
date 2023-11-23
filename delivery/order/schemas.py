import enum
from pydantic import BaseModel


class Status(enum.Enum):
    in_progress = 1
    completed = 2


class OrderRegister(BaseModel):
    name: str
    district: str


class OrderRegisterResponse(BaseModel):
    order_id: int
    courier_id: int


class OrderInfo(BaseModel):
    courier_id: int
    status: Status




