# pytest test_main.py -s

#pytest -m smoke -s
#pytest -m integration -s
#pytest -m db_config -s

# pytest test_main.py -k "behavior" -s
# Параметр -k в pytest — это мощный инструмент для фильтрации и выборочного запуска тестов по их имени.
# pytest ищет совпадение указанной строки без учета регистра в названиях функций, классов, файлов или параметризованных вариантов тестов.
# параметр -k поддерживает логические выражения and, or и not

# Флаги -x / --maxfail для остановки тестов при первой ошибке.
# Флаг --lf (--last-failed) для перезапуска только упавших тестов.
# Использование кастомных маркеров через ключ -m (альтернатива фильтрации по имени).

import pytest
import time

# Маркируем весь класс как integration
@pytest.mark.integration
class TestLifecycle:
    def test_first(self, session_resource, module_resource, class_resource, function_resource):
        print(f"-> Исполнение test_first. Доступно: {function_resource}")
        assert function_resource == "Новые данные"

    @pytest.mark.smoke # Этот тест одновременно и smoke, и integration
    def test_second(self, session_resource, module_resource, class_resource, function_resource):
        print("-> Исполнение test_second")
        assert True

def test_file_exception(safe_file_driver):
    print(f"-> Исполнение теста с файлом:{safe_file_driver.name} и данным в нем: {safe_file_driver.read_text()}")
    # Провоцируем падение теста для демонстрации работы try/finally в yield
    assert False 

@pytest.mark.smoke
def test_parametrized_db(db_driver):
    print(f"-> Тестирование логики с базой: {db_driver}")
    assert db_driver in ["PostgreSQL", "MySQL", "MongoDB"]

# В test_standard_behavior фикстура dynamic_environment выдаст дефолтный read-only.
def test_standard_behavior(dynamic_environment):
    # Фикстура benchmark_and_logger отработает сама (autouse)
    print(f"-> Выполнение стандартного теста. Окружение: {dynamic_environment}")
    time.sleep(0.1) # Специально задержим, чтобы autouse-фикстура замерила время
    assert dynamic_environment["mode"] == "read-only"

# В test_production_behavior посредством dynamic_environment объект request успешно перехватит строку "production" из декоратора и переключит режим на read-write.
@pytest.mark.db_config("production")
def test_production_behavior(dynamic_environment):
    # Тест помечен маркером, фикстура request прочитает это и изменит словарь
    print(f"-> Выполнение prod-теста. Окружение: {dynamic_environment}")
    assert dynamic_environment["mode"] == "read-write"
    assert dynamic_environment["timeout"] == 30

# ==========================================
# ДОПОЛНИТЕЛЬНЫЕ ВОЗМОЖНОСТИ PYTEST (для домашки)
# ==========================================

# 1. Параметризация самого теста (DDT - Data Driven Testing)
# Отличается от параметризации фикстуры тем, что данные передаются прямо в тест.
@pytest.mark.parametrize("username, password, expected", [
    ("admin", "admin123", True),
    ("admin", "wrongpass", False),
    ("", "", False)
])
def test_login_validation(username, password, expected):
    print(f"\n[DDT] Проверка логина: {username} / {password}")
    is_valid = (username == "admin" and password == "admin123")
    assert is_valid == expected


# 2. Проверка исключений (pytest.raises)
# Используется в негативном тестировании, когда мы ОЖИДАЕМ, что код упадет с ошибкой.
def test_division_by_zero():
    print("\n[Exception] Проверка деления на ноль")
    with pytest.raises(ZeroDivisionError):
        1 / 0


# 3. Пропуск теста (Skip)
# Если тест временно не работает или фича не готова.
@pytest.mark.skip(reason="Фича еще в разработке, тест временно отключен")
def test_future_feature():
    assert True


# 4. Ожидаемое падение (XFAIL)
# Если мы знаем, что тест упадет (баг известен), но хотим, чтобы PyTest не считал это ошибкой сборки.
@pytest.mark.xfail(reason="Известный баг #123: неверный расчет")
def test_known_bug():
    print("\n[XFAIL] Тест с известным багом")
    assert 2 + 2 == 5


# Запустить pytest lesson_materials/pytest_example_02/ -v -s
# Запуск только smoke тестов pytest lesson_materials/pytest_example_02/ -m smoke -v -s
# Запуск только Integration-тестов (маркер integration) pytest lesson_materials/pytest_example_02/ -m integration -v -s
# Запуск Фильтрация по имени (-k) pytest lesson_materials/pytest_example_02/ -k "behavior" -v -s
# Перезапуск только упавших тестов (--lf или --last-failed) pytest lesson_materials/pytest_example_02/ --lf -v -s
