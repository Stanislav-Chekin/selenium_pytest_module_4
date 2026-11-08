# pytest test_main.py -s

# pytest test_main.py -k "behavior" -s
# Параметр -k в pytest — это мощный инструмент для фильтрации и выборочного запуска тестов по их имени.
# pytest ищет совпадение указанной строки без учета регистра в названиях функций, классов, файлов или параметризованных вариантов тестов.
# параметр -k поддерживает логические выражения and, or и not

# Флаги -x / --maxfail для остановки тестов при первой ошибке.
# Флаг --lf (--last-failed) для перезапуска только упавших тестов.
# Использование кастомных маркеров через ключ -m (альтернатива фильтрации по имени).

# 1. Фикстуры как основа Setup / Teardown и области видимости (Scopes)
# Фикстуры управляют состоянием среды. Область видимости (scope) определяет, как часто (до после какого события) фикстура создается и уничтожается.

# 2. Возвращаемые значения (return vs yield) и обработка исключений
# return: Инициализирует ресурс, но не позволяет выполнить Teardown.
# yield: Разделяет фикстуру на этап настройки (до yield) и этап очистки (после yield). Если тест падает, код после yield все равно выполнится.

# 3. Фикстуры с параметрами (Parametrization)
# Параметризация фикстур позволяет запустить один и тот же тест несколько раз с разными входными данными.

# Главные правила работы с conftest.py:
# Никогда не импортируйте conftest: Строка from conftest import ... внутри тестовых файлов — это грубая ошибка,
# которая может привести к двойной инициализации фикстур и сбоям pytest.
# Pytest сам делает всю магию связывания.
# Иерархия папок: Вы можете создавать несколько файлов conftest.py на разных уровнях проекта.
# Фикстуры из корня доступны везде, а фикстуры из tests/api/conftest.py будут доступны только тестам внутри папки api/.
# Общие плагины: В conftest.py также принято выносить настройки конфигурации pytest, перехватчики (hooks) и регистрацию кастомных маркеров.

import pytest
import time

@pytest.fixture(scope="session")
def session_resource():
    print("\n[Setup] СЕССИЯ: Подключение к глобальной БД (один раз на все тесты)")
    yield "Глобальная БД"
    print("\n[Teardown] СЕССИЯ: Закрытие глобальной БД")

@pytest.fixture(scope="module")
def module_resource():
    print("\n[Setup] МОДУЛЬ: Инициализация тяжелого компонента модуля")
    yield "Компонент модуля"
    print("\n[Teardown] МОДУЛЬ: Очистка компонента модуля")

# Область package работает аналогично module, но инициализируется один раз для всей директории (пакета) с тестами при наличии там файла __init__.py.

@pytest.fixture(scope="class")
def class_resource():
    print("\n[Setup] КЛАСС: Создание изолированного контекста для класса")
    yield "Контекст класса"
    print("\n[Teardown] КЛАСС: Удаление контекста класса")

@pytest.fixture(scope="function")
def function_resource():
    print("\n[Setup] ФУНКЦИЯ: Генерация чистых тестовых данных")
    yield "Новые данные"
    print("\n[Teardown] ФУНКЦИЯ: Сброс данных")

# 2. Возвращаемые значения (return vs yield) и обработка исключений
@pytest.fixture
def safe_file_driver(tmp_path):
    # Setup
    print(f"\n[Setup] На вход safe_file_driver пришел: {tmp_path}")
    test_file = tmp_path / "log.txt"
    test_file.write_text("Initial data")
    print(f"Файл создан: {test_file}")
    
    try:
        yield test_file # Передаем ресурс тесту
    finally:
        # Teardown выполнится гарантированно, даже если тест упал с ошибкой
        print(f"\n[Teardown] Гарантированная очистка. Файл {test_file.name} существовал: {test_file.exists()}")

# 3. Фикстуры с параметрами (Parametrization)
@pytest.fixture(params=["PostgreSQL", "MySQL", "MongoDB"], ids=["pg", "my", "mongo"])
def db_driver(request):
    db_name = request.param
    print(f"\n[Setup] Подключение к {db_name}")
    yield db_name
    print(f"\n[Teardown] Отключение от {db_name}")

# Объект request предоставляет метаданные о выполняемом тесте.
# Через него можно:
# Читать параметры (request.param).
# Видеть имя теста (request.node.name).
# Проверять наличие кастомных маркеров на тесте (request.node.get_closest_marker).

# 4. Авто-фикстуры (autouse=True)
# Фикстуры с параметром autouse=True запускаются автоматически для всех тестов в их области видимости (scope), даже если они не указаны в аргументах теста явным образом.
# Это идеально подходит для настройки логов, очистки БД между тестами или замера времени.

@pytest.fixture(scope="function", autouse=True)
def benchmark_and_logger(request):
    # Setup: срабатывает ПЕРЕД каждым тестом
    start_time = time.time()
    print(f"\n[Autouse Setup] Старт теста: {request.node.name}")
    
    yield
    
    # Teardown: срабатывает ПОСЛЕ каждого теста
    duration = time.time() - start_time
    print(f"\n[Autouse Teardown] Тест {request.node.name} завершен за {duration:.4f} сек.")


# 5. Динамическая настройка через встроенную фикстуру requestОбъект request предоставляет метаданные о выполняемом тесте.
# Через него можно:
# Читать параметры (request.param).
# Видеть имя теста (request.node.name).
# Проверять наличие кастомных маркеров на тесте (request.node.get_closest_marker).
@pytest.fixture(scope="function")
def dynamic_environment(request):
    # Ищем маркер "db_config" на уровне вызывающего теста
    marker = request.node.get_closest_marker("db_config")
    
    # Конфигурация по умолчанию
    config = {"mode": "read-only", "timeout": 10}
    
    # Если маркер передан, переопределяем настройки
    if marker:
        print(f"\n[Request Setup] Найден маркер @pytest.mark.db_config с аргументами: {marker.args}")
        if "production" in marker.args:
            config["mode"] = "read-write"
            config["timeout"] = 30
    else:
        print("\n[Request Setup] Маркер db_config не найден. Применяются дефолтные настройки.")
        
    yield config
