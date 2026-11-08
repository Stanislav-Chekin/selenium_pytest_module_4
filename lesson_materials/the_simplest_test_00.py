import pytest

# 1. Тестируемый класс (обычно находится в вашем основном коде)
class Wallet:
    def __init__(self, balance=0):
        self.balance = balance

    def add_cash(self, amount):
        if amount < 0:
            raise ValueError("Нельзя добавить отрицательную сумму")
        self.balance += amount

    def spend_cash(self, amount):
        if amount > self.balance:
            raise ValueError("Недостаточно средств")
        self.balance -= amount
        return amount

# 2. Фикстура: подготовка тестовых данных ("заменяет" setUp - на самом деле в 99% дополняет SetUp)
@pytest.fixture
def empty_wallet():
    return Wallet()

@pytest.fixture
def wallet_with_cash():
    return Wallet(100)

# 3. Базовый тест
def test_default_initial_balance(empty_wallet):
    assert empty_wallet.balance == 0

# 4. Использование фикстур и проверка возвращаемого значения
def test_wallet_add_cash(empty_wallet):
    empty_wallet.add_cash(50)
    assert empty_wallet.balance == 50

# 5. Тестирование исключений
def test_wallet_spend_more_than_cash(wallet_with_cash):
    with pytest.raises(ValueError, match="Недостаточно средств"):
        wallet_with_cash.spend_cash(200)

# 6. Параметризация: запуск одного теста с разными данными
@pytest.mark.parametrize("amount, persent, date, expected", [
    (10, 5, (24,9,2027), 90),
    (50, 6, (24,9,2027), 50),
    (100, 3, (24,9,2027), 0),
])
def test_wallet_spend_exact_cash(wallet_with_cash, amount, persent, date, expected):
    wallet_with_cash.spend_cash(amount)
    print("we use these 2 variables:")
    print(persent)
    print(date)
    assert wallet_with_cash.balance == expected

# Чтобы увидеть сообщения print в консоли при запуске, обязательно используйте флаг -s (например, pytest -s the_simplest_test.py).
# Запустить pytest lesson_materials/the_simplest_test_00.py -v -s
