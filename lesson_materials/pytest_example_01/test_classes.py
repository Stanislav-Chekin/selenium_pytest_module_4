# pytest ОБНАРУЖИТ этот класс (начинается с Test, нет __init__)
class TestUserRegistration:

    # Метод будет обнаружен (начинается с test_)
    def test_valid_email(self):
        email = "student@university.edu"
        assert "@" in email

    # Метод будет обнаружен (начинается с test_)
    def test_password_length(self):
        password = "secret_password"
        assert len(password) >= 8

    # Этот метод будет ИГНОРИРОВАН (не начинается с test_)
    def utility_method(self):
        return True


# pytest ИГНОРИРУЕТ этот класс (название начинается с некорректного префикса)
class CheckPaymentStatus:

    def test_payment_success(self):
        assert True


# pytest ВЫЗОВЕТ ПРЕДУПРЕЖДЕНИЕ / ОШИБКУ при запуске (содержит __init__)
class TestInvalidClassStructure:

    def __init__(self):
        self.status = "init_block"

    # Этот тест не запустится из-за наличия __init__ в классе
    def test_some_logic(self):
        assert self.status == "init_block"

# Количество тестов: Pytest найдет ровно 5 тестов (3 из файла функций и 2 из класса TestUserRegistration).
# Игнорирование: Функции и классы без префикса test_ / Test будут молча пропущены.
# Предупреждение (Warning): В разделе PytestCollectionWarning отобразится четкое предупреждение о том, что класс TestInvalidClassStructure не может быть запущен,
#  так как у него есть конструктор __init__. Это классическая ошибка новичков.

# pip install --upgrade --force-reinstall --no-cache-dir pytest
# pytest --version
# Запустить pytest lesson_materials/pytest_example_01/test_classes.py -v
