import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


def shift_month(month_name, year, delta):
    """Посчитать, какой месяц и год должны быть после сдвига на delta месяцев.

    Пример: shift_month("December", 2026, +1) -> ("January", "2027").
    Нужна, чтобы в тестах сравнивать с ТОЧНЫМ ожидаемым значением,
    а не просто «значение изменилось».
    """
    index = MONTHS.index(month_name) + int(year) * 12 + delta
    return MONTHS[index % 12], str(index // 12)


class CalendarsPage(BasePage):
    """Страница https://practice-automation.com/calendars/"""

    URL = "https://practice-automation.com/calendars/"

    DATE_INPUT = (By.ID, "g1065-1-selectorenteradate")
    ERROR_MESSAGE = (By.ID, "g1065-1-selectorenteradate-text-error-message")

    DATEPICKER = (By.CSS_SELECTOR, ".dp-cal")
    NEXT_BUTTON = (By.CSS_SELECTOR, "button.dp-next")
    PREV_BUTTON = (By.CSS_SELECTOR, "button.dp-prev")
    MONTH_BUTTON = (By.CSS_SELECTOR, "button.dp-cal-month")
    YEAR_BUTTON = (By.CSS_SELECTOR, "button.dp-cal-year")
    DAY_BUTTONS = (By.CSS_SELECTOR, "button.dp-day:not(.dp-edge-day)")
    MONTH_ITEMS = (By.CSS_SELECTOR, "button.dp-month")

    @allure.step("Открыть страницу Calendars")
    def open(self):
        self.open_page(self.URL, self.DATE_INPUT)

    @allure.step("Открыть календарь кликом по полю даты")
    def open_datepicker(self):
        self.click(self.DATE_INPUT)
        self.wait.until(EC.visibility_of_element_located(self.DATEPICKER))

    @allure.step("Нажать стрелку «следующий месяц»")
    def click_next_month(self):
        self.click(self.NEXT_BUTTON)

    @allure.step("Нажать стрелку «предыдущий месяц»")
    def click_prev_month(self):
        self.click(self.PREV_BUTTON)

    @allure.step("Кликнуть на число {day_number} в текущем месяце")
    def click_day(self, day_number):
        days = self.find_all(self.DAY_BUTTONS)
        for day in days:
            if day.text == str(day_number):
                day.click()
                return
        raise ValueError(f"День {day_number} не найден в текущем месяце")

    @allure.step("Ввести в поле даты: {text}")
    def type_date(self, text):
        self.type_text(self.DATE_INPUT, text)

    @allure.step("Убрать фокус с поля даты (Tab)")
    def blur_date_input(self):
        self.find(self.DATE_INPUT).send_keys(Keys.TAB)

    def get_input_value(self):
        return self.find(self.DATE_INPUT).get_attribute("value")

    @allure.step("Прочитать сообщение об ошибке")
    def get_error_message(self):
        self.wait.until(lambda d: self.find(self.ERROR_MESSAGE).text.strip() != "")
        return self.find(self.ERROR_MESSAGE).text

    def get_current_month_year(self):
        """Вернуть (месяц, год) из шапки календаря, например ("January", "2027")."""
        month = self.find(self.MONTH_BUTTON).text
        year = self.find(self.YEAR_BUTTON).text
        return month, year

    @allure.step("Дождаться в шапке календаря: {expected}")
    def wait_for_month_year(self, expected):
        """Подождать, пока шапка покажет (месяц, год) = expected, и вернуть то, что показано.

        Если время вышло — не падаем здесь, а возвращаем реальное значение,
        чтобы assert в тесте показал понятное «ожидали X, получили Y».
        """
        try:
            self.wait.until(lambda d: self.get_current_month_year() == expected)
        except TimeoutException:
            pass
        return self.get_current_month_year()

    @allure.step("Выбрать месяц {month_name} из списка")
    def select_month(self, month_name):
        self.click(self.MONTH_BUTTON)
        items = self.find_all(self.MONTH_ITEMS)
        for item in items:
            if item.text == month_name:
                item.click()
                return
        raise ValueError(f"Месяц {month_name} не найден в списке")

    def open_year_picker(self):
        self.click(self.YEAR_BUTTON)

    @allure.step("Выбрать год {year} из списка")
    def select_year(self, year):
        self.open_year_picker()
        locator = (By.CSS_SELECTOR, f"button.dp-year[data-year='{year}']")
        element = self.wait.until(EC.presence_of_element_located(locator))
        # Список лет длинный и скроллится — кнопка нужного года может быть вне экрана.
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        element.click()

    @allure.step("Дождаться в шапке календаря года {year}")
    def wait_for_year(self, year):
        try:
            self.wait.until(lambda d: self.get_current_month_year()[1] == str(year))
        except TimeoutException:
            pass
        return self.get_current_month_year()[1]

    @allure.step("Дождаться, что в поле даты появилось значение")
    def wait_for_input_value(self, expected):
        try:
            self.wait.until(lambda d: self.get_input_value() == expected)
        except TimeoutException:
            pass
        return self.get_input_value()
