import pytest
import os
from datetime import datetime
from selenium import webdriver
from selenium_tests.pages.text_box_page import TextBoxPage


# 1. Фикстура для запуска и закрытия браузера
@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


# 2. Фикстура для Page Object (чтобы не писать page = TextBoxPage(driver) в каждом тесте)
@pytest.fixture(scope="function")
def text_box_page(driver):
    return TextBoxPage(driver)


# 3. Хук для создания скриншота при падении теста (ФИШКА ДЛЯ ДОМАШКИ)
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    # Если тест упал на этапе вызова (выполнения)
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            # Создаем папку для скриншотов, если ее нет
            if not os.path.exists("screenshots"):
                os.makedirs("screenshots")

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_name = f"screenshots/fail_{item.name}_{timestamp}.png"
            driver.save_screenshot(file_name)
            print(f"\n[СКРИНШОТ] Тест упал! Скриншот сохранен: {file_name}")
