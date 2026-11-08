from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class TextBoxPage:
    URL = "https://qa-guru.github.io/one-page-form/text-box.html"

    # Локаторы элементов формы
    FULL_NAME = (By.ID, "userName")
    EMAIL = (By.ID, "userEmail")
    CURRENT_ADDRESS = (By.ID, "currentAddress")
    PERMANENT_ADDRESS = (By.ID, "permanentAddress")
    SUBMIT_BUTTON = (By.ID, "submit")

    # Локаторы результирующего блока (вывода данных)
    OUTPUT_BOX = (By.ID, "output")
    OUTPUT_NAME = (By.ID, "name")
    OUTPUT_EMAIL = (By.ID, "email")
    OUTPUT_CUR_ADDR = (By.CSS_SELECTOR, "#output #currentAddress")
    OUTPUT_PERM_ADDR = (By.CSS_SELECTOR, "#output #permanentAddress")

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)
        return self  # Fluent Interface

    def fill_form(self, name=None, email=None, cur_addr=None, perm_addr=None):
        if name is not None:
            full_name_field = self.driver.find_element(*self.FULL_NAME)
            full_name_field.clear()
            full_name_field.send_keys(name)
        if email is not None:
            self.driver.find_element(*self.EMAIL).send_keys(email)
        if cur_addr is not None:
            self.driver.find_element(*self.CURRENT_ADDRESS).send_keys(cur_addr)
        if perm_addr is not None:
            self.driver.find_element(*self.PERMANENT_ADDRESS).send_keys(perm_addr)
        return self  # Fluent Interface

    def submit(self):
        button = self.driver.find_element(*self.SUBMIT_BUTTON)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
        button.click()
        return self  # Fluent Interface

    def get_output_data(self):
        try:
            WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located(self.OUTPUT_BOX)
            )
        except TimeoutException:
            return None

        name = self.driver.find_element(*self.OUTPUT_NAME).text.split(":", 1)[-1].strip()
        email = self.driver.find_element(*self.OUTPUT_EMAIL).text.split(":", 1)[-1].strip()
        cur_addr = self.driver.find_element(*self.OUTPUT_CUR_ADDR).text.split(":", 1)[-1].strip()
        perm_addr = self.driver.find_element(*self.OUTPUT_PERM_ADDR).text.split(":", 1)[-1].strip()

        return {"name": name, "email": email, "cur_addr": cur_addr, "perm_addr": perm_addr}

    def is_email_error_present(self):
        email_field = self.driver.find_element(*self.EMAIL)
        field_class = email_field.get_attribute("class")

        if field_class is None:
            return False

        return "field-error" in field_class or "error" in field_class
