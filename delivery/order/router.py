from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException

from delivery.courier.models import Courier
from delivery.database import get_db
from delivery.order.models import Order
from delivery.order.schemas import (OrderRegisterResponse, OrderRegister, OrderInfo, Status)

router = APIRouter()


@router.post('/order', response_model=Optional[OrderRegisterResponse])
def order_register(order_data: OrderRegister, db: Session = Depends(get_db)):
    """
    Регистрация заказа в системе.
    """
    free_courier = db.query(Courier).filter(
        Courier.active_order == None,
        Courier.districts.contains([order_data.district])
    ).first()
    if not free_courier:
        raise HTTPException(status_code=404, detail="Courier not found")
    order = Order(**order_data.model_dump(), courier_id=free_courier.id)
    db.add(order)
    db.commit()
    data = {
        "order_id": order.id,
        "courier_id": order.courier_id
    }
    return data


@router.get('/order/{id}', response_model=OrderInfo)
def order_info(id: int, db: Session = Depends(get_db)):
    """
    Получение информации о заказе
    """
    order = db.query(Order).filter(Order.id == id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")

    data = {
        "courier_id": order.courier_id,
        "status": order.status
    }
    return data


@router.post('/order/{id}')
def complete_order(id: int, db: Session = Depends(get_db)):
    """
    Завершить заказ. Вернёт ошибку, если заказ уже завершён или такого заказа нет.
    """
    order = (
        db.query(Order)
        .filter(Order.id == id, Order.status == Status.in_progress)
        .first()
    )
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found or already completed.")

    order.status = Status.completed
    order.end_time = datetime.utcnow()
    db.commit()
    return f'Order {order.id} completed'



