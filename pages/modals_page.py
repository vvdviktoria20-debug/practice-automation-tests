import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class ModalsPage(BasePage):
    """Страница https://practice-automation.com/modals/"""

    URL = "https://practice-automation.com/modals/"

    SIMPLE_MODAL_BUTTON = (By.XPATH, "//*[self::a or self::button][normalize-space()='Simple Modal']")
    FORM_MODAL_BUTTON = (By.XPATH, "//*[self::a or self::button][normalize-space()='Form Modal']")

    ACTIVE_MODAL = (By.CSS_SELECTOR, ".pum-overlay.pum-active")
    ACTIVE_MODAL_CONTENT = (By.CSS_SELECTOR, ".pum-overlay.pum-active .pum-content")
    CLOSE_BUTTON = (By.CSS_SELECTOR, ".pum-overlay.pum-active .pum-close")

    NAME_INPUT = (By.CSS_SELECTOR, ".pum-overlay.pum-active input[type='text']")
    EMAIL_INPUT = (By.CSS_SELECTOR, ".pum-overlay.pum-active input[type='email']")
    MESSAGE_INPUT = (By.CSS_SELECTOR, ".pum-overlay.pum-active textarea")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, ".pum-overlay.pum-active button[type='submit']")

    # Сообщение об успешной отправке формы — ищем именно элемент с этим текстом.
    SUCCESS_MESSAGE = (By.XPATH, "//*[contains(normalize-space(text()), 'Thank you for your response')]")

    @allure.step("Открыть страницу Modals")
    def open(self):
        self.open_page(self.URL, self.SIMPLE_MODAL_BUTTON)

    @allure.step("Открыть простое модальное окно (Simple Modal)")
    def open_simple_modal(self):
        self.click(self.SIMPLE_MODAL_BUTTON)
        self.wait.until(EC.visibility_of_element_located(self.ACTIVE_MODAL))

    @allure.step("Открыть модальное окно с формой (Form Modal)")
    def open_form_modal(self):
        self.click(self.FORM_MODAL_BUTTON)
        self.wait.until(EC.visibility_of_element_located(self.ACTIVE_MODAL))

    @allure.step("Закрыть модальное окно кнопкой ×")
    def close_modal(self):
        self.click(self.CLOSE_BUTTON)
        self.wait.until(EC.invisibility_of_element_located(self.ACTIVE_MODAL))

    def is_modal_open(self):
        modals = self.driver.find_elements(*self.ACTIVE_MODAL)
        return len(modals) > 0 and modals[0].is_displayed()

    @allure.step("Прочитать текст модального окна")
    def get_modal_text(self):
        self.wait.until(lambda d: self.find(self.ACTIVE_MODAL_CONTENT).text.strip() != "")
        return self.find(self.ACTIVE_MODAL_CONTENT).text

    @allure.step("Заполнить форму (name='{name}', email='{email}', message='{message}')")
    def fill_form(self, name="", email="", message=""):
        if name:
            self.type_text(self.NAME_INPUT, name)
        if email:
            self.type_text(self.EMAIL_INPUT, email)
        if message:
            self.type_text(self.MESSAGE_INPUT, message)

    @allure.step("Нажать Submit")
    def submit_form(self):
        self.click(self.SUBMIT_BUTTON)

    @allure.step("Дождаться сообщения об успешной отправке и прочитать его")
    def get_success_message(self):
        """Ждём появления конкретного элемента с текстом «Thank you for your response»."""
        element = self.wait.until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE))
        return element.text

    def get_page_text(self):
        return self.driver.find_element(By.TAG_NAME, "body").text
