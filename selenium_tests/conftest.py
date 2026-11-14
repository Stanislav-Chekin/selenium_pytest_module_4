import pytest
import os
from datetime import datetime
from selenium import webdriver
import allure  # ДОБАВИЛИ ИМПОРТ
from selenium_tests.pages.text_box_page import TextBoxPage


# 1. Фикстура для запуска и закрытия браузера
@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


# 2. Фикстура для Page Object
@pytest.fixture(scope="function")
def text_box_page(driver):
    return TextBoxPage(driver)


# 3. Хук для создания скриншота при падении теста
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    # Если тест упал на этапе вызова (выполнения)
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            # Сохраняем локально (опционально, для истории)
            if not os.path.exists("screenshots"):
                os.makedirs("screenshots")

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_name = f"screenshots/fail_{item.name}_{timestamp}.png"
            driver.save_screenshot(file_name)

            # ФИШКА ALLURE: Прикрепляем скриншот прямо в отчет!
            allure.attach(
                driver.get_screenshot_as_png(),
                name=f"Скриншот падения: {item.name}",
                attachment_type=allure.attachment_type.PNG
            )
            print(f"\n[СКРИНШОТ] Тест упал! Скриншот сохранен: {file_name} и прикреплен в Allure.")
