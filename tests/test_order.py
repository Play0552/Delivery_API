from conftest import client, TestingSessionLocal
from delivery.courier.models import Courier


class TestOrder:
    test_courier_id = 75
    def test_add_courier(self):
        with TestingSessionLocal() as db:
            test_courier = Courier(
                id=self.test_courier_id,
                name="Никита",
                districts=["district99"]
            )
            db.add(test_courier)
            db.commit()
            result = db.query(Courier).filter(Courier.id == self.test_courier_id).first()
            assert result.name == "Никита", "Курьер не добавлен"

    def test_order_register(self):
        """
        Проверка запроса на создание заказа
        """
        response = client.post("/order", json={
            "name": "Eda",
            "district": "district99"
        })
        response_2 = client.post("/order", json={
            "name": "Eda2",
            "district": "district99"
        })
        assert response.status_code == 200, "Заказ не добавился, хотя курьер свободен"
        assert response_2.status_code == 404, "Заказ добавился занятому курьеру"
        assert response.json()["courier_id"] == self.test_courier_id, "Заказ добавился курьеру, с другим регионом"

    def test_order_info(self):
        """
        Проверка запроса на получение информации о заказе
        """
        response = client.get("/order/1")
        assert response.status_code == 200, "Ошибка получения информации о заказе"
        assert response.json()["courier_id"] == self.test_courier_id, "Заказ назначился не тому курьеру"

        response_2 = client.get("/order/1000")
        assert response_2.status_code == 404, "Найден не существующий заказ"


    def test_complete_order(self):
        """
        Проверка запроса на завершение заказа
        """
        response = client.post("/order/1")
        assert response.status_code == 200, "Не удаётся завершить заказ"
        assert response.json() == "Order 1 completed", "Не удаётся завершить заказ"

        response = client.post("/order/1")
        assert response.status_code == 404, "Завершается уже завершённый или несуществующий заказ"



