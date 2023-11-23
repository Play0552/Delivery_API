from datetime import timedelta
from functools import reduce

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from delivery.database import get_db
from delivery.courier.models import Courier
from delivery.courier.schemas import (CourierRegister, CouriersInfo, CourierInfo)
from delivery.order.models import Order
from delivery.order.schemas import Status

router = APIRouter()


@router.post('/courier')
def courier_register(courier_data: CourierRegister, db: Session = Depends(get_db)):
    """
    Регистрация курьера в системе.
    """
    new_courier = Courier(**courier_data.model_dump())
    db.add(new_courier)
    db.commit()
    return f'Поздравляю {new_courier.name}, вы успешно зарегистрировались. Ваш ID: {new_courier.id}'


@router.get('/courier', response_model=list[CouriersInfo])
def couriers_info(db: Session = Depends(get_db)):
    """
    Получение информации о всех курьерах в системе
    """
    couriers = db.query(Courier).all()
    return couriers


@router.get('/courier/{id}', response_model=CourierInfo)
def courier_info(id: int, db: Session = Depends(get_db)):
    """
    Получение подробной информации о курьере
    """
    courier = db.query(Courier).filter(Courier.id == id).first()
    if not courier:
        raise HTTPException(404, "Неправильный ID курьера")

    if courier.active_order:
        active_order = {
            "order_id": courier.active_order[0].id,
            "order_name": courier.active_order[0].name
        }
    else:
        active_order = None

    completed_orders = db.query(Order).filter(Order.courier_id == id, Order.status == Status.completed).all()
    if completed_orders:
        total_time = reduce(lambda c, x: c + x, [(order.end_time - order.start_time) for order in completed_orders])
        avg_timedelta = (total_time / len(completed_orders)).total_seconds()
        avg_order_complete_time = timedelta(seconds=int(avg_timedelta))
    else:
        avg_order_complete_time = None

    completed_orders_per_day = (
        db.query(func.count(Order.id))
        .filter(Order.courier_id == id, Order.status == Status.completed)
        .group_by(func.date_trunc('day', Order.end_time))
        .all()
    )
    if completed_orders_per_day:
        total_orders = sum(count[0] for count in completed_orders_per_day)
        avg_day_orders = total_orders / len(completed_orders_per_day)
    else:
        avg_day_orders = None

    courier_data = {
        "id": courier.id,
        "name": courier.name,
        "active_order": active_order,
        "avg_order_complete_time": avg_order_complete_time,
        "avg_day_orders": avg_day_orders
    }
    return courier_data



