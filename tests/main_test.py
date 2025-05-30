from fastapi.testclient import TestClient
import pytest
from app.app import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Калькулятор" in response.text
    assert "Сложение" in response.text

def test_add():
    response = client.get("/2+3")
    assert response.status_code == 200
    assert "2 + 3 = 5" in response.text

    response = client.get("/2.5+3.5")
    assert response.status_code == 200
    assert "2.5 + 3.5 = 6" in response.text

def test_subtract():
    response = client.get("/5-3")
    assert response.status_code == 200
    assert "5 - 3 = 2" in response.text

    response = client.get("/3.5-1.5")
    assert response.status_code == 200
    assert "3.5 - 1.5 = 2" in response.text

def test_multiply():
    response = client.get("/2*3")
    assert response.status_code == 200
    assert "2 * 3 = 6" in response.text

    response = client.get("/2.5*4")
    assert response.status_code == 200
    assert "2.5 * 4 = 10" in response.text

def test_divide():
    response = client.get("/6/3")
    assert response.status_code == 200
    assert "6 / 3 = 2" in response.text

    response = client.get("/5/2")
    assert response.status_code == 200
    assert "5 / 2 = 2.5" in response.text

    response = client.get("/10/0")
    assert response.status_code == 400
    assert response.text == "Ошибка: Деление на ноль невозможно"

def test_random_number():
    response = client.get("/random/1/10")
    assert response.status_code == 200
    assert "Случайное число в диапазоне [1, 10)" in response.text

    response = client.get("/random/10/1")
    assert response.status_code == 400
    assert "Минимум должен быть меньше максимума" in response.text

def test_logarithm():
    response = client.get("/log/2/8")
    assert response.status_code == 200
    assert "log_2(8) = 3" in response.text

    response = client.get("/log/0/10")
    assert response.status_code == 400
    assert response.text == "Ошибка: Оба числа должны быть положительными"

    response = client.get("/log/1/10")
    assert response.status_code == 400
    assert response.text == "Ошибка: Основание логарифма не может быть равно 1"

    response = client.get("/log/-2/8")
    assert response.status_code == 400
    assert response.text == "Ошибка: Оба числа должны быть положительными"

    response = client.get("/log/2/-8")
    assert response.status_code == 400
    assert response.text == "Ошибка: Оба числа должны быть положительными"


def test_percent():
    response = client.get("/50/%/200")
    assert response.status_code == 200
    assert "50 составляет 25% от 200" in response.text

    response = client.get("/0/%/200")
    assert response.status_code == 400
    assert "Числа должны быть > 0" in response.text

    response = client.get("/50/%/0")
    assert response.status_code == 400
    assert "Числа должны быть > 0" in response.text