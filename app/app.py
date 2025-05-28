from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
import random
import math
app = FastAPI()

def isint(res):
    if res.is_integer():
        res = int(res)
    return res

@app.get("/", response_class=PlainTextResponse)
def read():
    return """
        Калькулятор

        Доступные функции:
        Сложение: /a+b
        Вычитание: /a-b
        Умножение: /a*b
        Деление: /a/b
        Случайное число в промежутке /random/a/b
        log_a(b) /log/a/b
        Процент от числа /a/%/b
        """

@app.get("/{a}+{b}", response_class=PlainTextResponse)
def add(a: float, b: float):
    return (f"{isint(a)} + {isint(b)} = {isint(a+b)}")

@app.get("/{a}-{b}",response_class=PlainTextResponse)
def subtract(a: float, b: float):
    return (f"{isint(a)} - {isint(b)} = {isint(a-b)}")

@app.get("/{a}*{b}",response_class=PlainTextResponse)
def multiply(a: float, b: float):
    return (f"{isint(a)} * {isint(b)} = {isint(a*b)}")

@app.get("/{a}/{b}", response_class=PlainTextResponse)
def divide(a: float, b: float):
    if b == 0:
        return PlainTextResponse(
            content="Ошибка: Деление на ноль невозможно",
            status_code=400
        )
    result = a / b
    return f"{isint(a)} / {isint(b)} = {isint(result)}"

@app.get("/random/{a}/{b}", response_class=PlainTextResponse)
def random_number(a: float, b: float):
    if a >= b:
        raise HTTPException(status_code=400, detail="Минимум должен быть меньше максимума")
    result = random.uniform(a, b)
    return f"Случайное число в диапазоне [{isint(a)}, {isint(b)}) = {isint(result)}"

@app.get("/log/{a}/{b}", response_class=PlainTextResponse)
def logarithm(a: float, b: float):
    if a <= 0 or b <= 0:
        return PlainTextResponse(
            content="Ошибка: Оба числа должны быть положительными",
            status_code=400
        )
    if a == 1:
        return PlainTextResponse(
            content="Ошибка: Основание логарифма не может быть равно 1",
            status_code=400
        )
    result = math.log(b, a)
    return f"log_{isint(a)}({isint(b)}) = {isint(result)}"

@app.get("/{a}/%/{b}", response_class=PlainTextResponse)
def percent(a: float, b: float):
    if a <= 0 or b <=0:
        raise HTTPException(status_code=400, detail="Числа должны быть > 0")
    result = (a / b) * 100
    return f"{isint(a)} составляет {isint(result)}% от {isint(b)}"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1", port=8000)