import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage

_UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
_LOWER = "abcdefghijklmnopqrstuvwxyz"


class FormFieldsPage(BasePage):
    """Страница с формой https://practice-automation.com/form-fields/

    Пункт 5 задания: получить список элементов из блока «Automation tools»,
    преобразовать в текст и записать в поле Message через запятую.
    """

    URL = "https://practice-automation.com/form-fields/"

    # Элементы списка «Automation tools»: находим заголовок блока (без учёта регистра)
    # и берём пункты <li> ближайшего за ним списка. Не привязано к id/классам.
    AUTOMATION_TOOLS_ITEMS = (
        By.XPATH,
        f"(//*[normalize-space(translate(text(), '{_UPPER}', '{_LOWER}'))='automation tools'])[1]"
        "/following::ul[1]/li",
    )

    # Поле Message — textarea формы на странице.
    MESSAGE_TEXTAREA = (By.CSS_SELECTOR, "textarea")

    @allure.step("Открыть страницу Form Fields")
    def open(self):
        self.driver.get(self.URL)

    @allure.step("Получить список элементов из блока «Automation tools»")
    def get_automation_tools(self):
        """Вернуть названия инструментов списком строк, например ['Selenium', 'Playwright', ...]."""
        elements = self.find_all(self.AUTOMATION_TOOLS_ITEMS)
        # textContent надёжнее .text: не зависит от того, виден ли элемент на экране.
        tools = [el.get_attribute("textContent").strip() for el in elements]
        return [tool for tool in tools if tool]

    @allure.step("Заполнить поле Message текстом: {text}")
    def fill_message(self, text):
        self.type_text(self.MESSAGE_TEXTAREA, text)

    @allure.step("Прочитать значение поля Message")
    def get_message_value(self):
        return self.find(self.MESSAGE_TEXTAREA).get_attribute("value")

    @allure.step("Заполнить Message списком Automation tools через запятую")
    def fill_message_with_automation_tools(self):
        """Собрать список инструментов, превратить в строку «A, B, C» и вписать в Message."""
        tools = self.get_automation_tools()
        text = ", ".join(tools)
        self.fill_message(text)
        return tools, text
