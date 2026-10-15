import time

import allure
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """Базовый класс для всех страниц — общие методы."""

    def __init__(self, driver):
        self.driver = driver
        # 20 секунд: запас на медленный сайт и сеть; ожидание всё равно
        # заканчивается сразу, как только элемент появился.
        self.wait = WebDriverWait(driver, 20)

    def open(self, url):
        with allure.step(f"Открыть страницу {url}"):
            self.driver.get(url)

    def open_page(self, url, ready_locator):
        """Открыть страницу и убедиться, что она реально загрузилась.

        Сайт иногда отвечает с задержкой или отдаёт недогруженную страницу.
        Если нужный элемент не появился — один раз перезагружаем страницу.
        """
        with allure.step(f"Открыть страницу {url}"):
            self.driver.get(url)
            try:
                self.wait.until(EC.visibility_of_element_located(ready_locator))
            except TimeoutException:
                self.driver.refresh()
                self.wait.until(EC.visibility_of_element_located(ready_locator))

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        """Надёжный клик: прокручиваем к элементу и кликаем.

        Если в момент клика элемент кратко перекрыт (например, ещё идёт анимация
        появления окна), ждём и пробуем ещё раз, а в крайнем случае кликаем через JS.
        """
        with allure.step(f"Нажать на элемент {locator[1]}"):
            element = self.wait.until(EC.element_to_be_clickable(locator))
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", element)
            for _ in range(3):
                try:
                    element.click()
                    return
                except ElementClickInterceptedException:
                    time.sleep(0.5)
                    element = self.wait.until(EC.element_to_be_clickable(locator))
            self.driver.execute_script("arguments[0].click();", element)

    def type_text(self, locator, text):
        with allure.step(f"Ввести «{text}» в поле {locator[1]}"):
            element = self.find(locator)
            element.clear()
            element.send_keys(text)
