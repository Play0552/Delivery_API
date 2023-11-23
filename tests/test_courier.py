from conftest import client, TestingSessionLocal
from delivery.courier.models import Courier
from delivery.order.models import Order
from datetime import datetime


class TestCourier:
    def test_data_add(self):
        """
        Создание тестового курьера и заказа для этого курьера
        """
        with TestingSessionLocal() as db:
            test_courier = Courier(
                id=333,
                name="Вика",
                districts=["district2"]
            )
            db.add(test_courier)
            test_order = Order(
                id=20,
                name="Тяжести",
                district=["district2"],
                status="completed",
                start_time=datetime(2022, 10, 20, 3, 15, 40),
                end_time=datetime(2022, 10, 20, 4, 15, 40),
                courier_id=333
            )
            test_order_2 = Order(
                id=21,
                name="Hleb",
                district=["district2"],
                status="in_progress",
                start_time=datetime(2022, 10, 20, 5, 15, 40),
                end_time=None,
                courier_id=333
            )

            db.add_all([test_order, test_order_2])
            db.commit()
            order = db.query(Order).filter(Order.id == 21).first()
            assert order.name == "Hleb", "Заказ не добавлен"
            assert order.courier.name == "Вика", "Ошибка имени курьера при добавлении заказа"

    def test_courier_register(self):
        """
        Запрос на регистрацию курьера
        """
        response = client.post("/courier", json={
            "name": "Коля",
            "districts": [
                "district2", "district3"
            ]
        })
        assert response.json() == "Поздравляю Коля, вы успешно зарегистрировались. Ваш ID: 1"
        assert response.status_code == 200, "Ошибка добавления пользователя"

    def test_couriers_info(self):
        """
        Запрос на получение информации о всех курьерах
        """
        response = client.get("/courier")
        assert response.status_code == 200
        assert response.json()[1]["name"] == "Коля", "Не удаётся получить информацию о курьерах"

    def test_courier_info(self):
        """
        Запрос на получение информации о конкретном курьере
        """
        response = client.get("/courier/1")
        assert response.status_code == 200, "Существующий курьер не обнаружен"
        assert response.json()["name"] == "Коля"

        response_2 = client.get("/courier/999")
        assert response_2.status_code == 404, "Найден несуществующий курьер"

        response_3 = client.get("courier/333")
        expected_response_3 = {
            "id": 333,
            "name": "Вика",
            "active_order": {'order_id': 21, 'order_name': 'Hleb'},
            "avg_order_complete_time": "PT3600S",
            "avg_day_orders": 1.0
        }
        assert response_3.json() == expected_response_3
