from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """Базовый класс для всех страниц — общие методы."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # ждём элемент до 10 секунд

    def open(self, url):
        self.driver.get(url)

    def find(self, locator):
        """Найти один элемент, дождавшись его появления."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator):
        """Найти список элементов."""
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def type_text(self, locator, text):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)