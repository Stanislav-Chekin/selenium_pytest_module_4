import pytest
from dataclasses import dataclass

# pytest .\test_with_data_class_03.py -s

@dataclass
class Product:
    name: str
    price: float
    quantity: int = 1  # Значение по умолчанию

@pytest.fixture
def expected_product():
    return Product(name="Смартфон", price=30000.0)

def test_product_creation(expected_product):
    # Демонстрация возможностей @dataclass
    print("") # New line

    # 1. Автоматический конструктор __init__
    prod1 = Product(name="Ноутбук", price=75000.0, quantity=2)
    prod2 = Product(name="Мышь", price=1500.0)  # quantity возьмется по умолчанию (1)
    prod3 = Product(name="Ноутбук", price=75000.0, quantity=2)

    # 2. Автоматическое красивое выведение строки __repr__
    print(prod1)  
    # Выведет: Product(name='Ноутбук', price=75000.0, quantity=2)

    # 3. Автоматическое сравнение по значениям полей __eq__
    print(prod1 == prod3)  # Выведет: True (значения всех полей совпадают)
    print(prod1 == prod2)  # Выведет: False

    # Какая-то бизнес-логика, возвращающая объект
    actual_product = Product(name="Смартфон", price=30000.0)
    
    print(actual_product)
    print(expected_product)
    
    # Благодаря dataclass, мы можем сравнивать объекты одной строкой
    assert actual_product == expected_product

# запустить pytest lesson_materials/test_with_data_class_03.py -v -s
