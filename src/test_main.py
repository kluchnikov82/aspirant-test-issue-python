"""В данном модуле происходит тестировние следующих API-сервисов:
1. Получение списка городов.
2. Получение списка пользователей.
3. Получение списка всех пикников.
4. Создание города по его названию.
5. Регистрация пользователя.
6. Добавление нового объекта пикник в БД.
7. Регистрация пользователя на пикник.
"""
from fastapi.testclient import TestClient
from main import app
import logging


logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger('logger_root')  # pylint: disable=invalid-name

client = TestClient(app)

def test_get_cities():
    """Получение списка городов"""
    response = client.get("/get-cities/", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    logger.info(
        f'Тест get_cities() пройден успешно!'
    )

def test_users_list():
    """Получение списка пользователей"""
    response = client.get("/users-list/?minimum=25&maximum=40", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    logger.info(
        f'Тест users_list() пройден успешно!'
    )

def test_all_picnics():
    """Получение списка всех пикников"""
    response = client.get("/all-picnics/", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    logger.info(
        f'Тест all_picnics() пройден успешно!'
    )

def test_create_city():
    """Создание города по его названию"""
    response = client.post(
        "/create-city/",
        headers={"X-Token": "coneofsilence"},
        json={"city": "Сочи"},
    )
    assert response.status_code == 201
    logger.info(
        f'Тест create_city() пройден успешно!'
    )


def test_register_user():
    """Регистрация пользователя"""
    response = client.post(
        "/register-user/",
        headers={"X-Token": "coneofsilence"},
        json={"name": "Иван", "surname": "Петров", "age": "29"},
    )
    assert response.status_code == 201
    logger.info(
        f'Тест register_user() пройден успешно!'
    )

def test_picnic_add():
    """Добавление нового объекта пикник в БД"""
    response = client.post(
        "/picnic-add/",
        headers={"X-Token": "coneofsilence"},
        json={"city_id": "2", "time": "2021-05-06 09:56:14"},
    )
    assert response.status_code == 201
    logger.info(
        f'Тест picnic_add() пройден успешно!'
    )

def test_picnic_register():
    """Регистрация пользователя на пикник"""
    response = client.post(
        "/picnic-register/",
        headers={"X-Token": "coneofsilence"},
        json={"user_id": "2", "picnic_id": "3"},
    )
    assert response.status_code == 201
    logger.info(
        f'Тест picnic_register() пройден успешно!'
    )


