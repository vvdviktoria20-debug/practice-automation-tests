from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


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

    def open(self):
        self.driver.get(self.URL)

    def open_datepicker(self):
        self.click(self.DATE_INPUT)
        self.wait.until(EC.visibility_of_element_located(self.DATEPICKER))

    def click_next_month(self):
        self.click(self.NEXT_BUTTON)

    def click_prev_month(self):
        self.click(self.PREV_BUTTON)

    def click_day(self, day_number):
        """Кликнуть на число в текущем показанном месяце."""
        days = self.find_all(self.DAY_BUTTONS)
        for day in days:
            if day.text == str(day_number):
                day.click()
                return
        raise ValueError(f"День {day_number} не найден в текущем месяце")

    def type_date(self, text):
        self.type_text(self.DATE_INPUT, text)

    def blur_date_input(self):
        self.find(self.DATE_INPUT).send_keys(Keys.TAB)

    def get_input_value(self):
        return self.find(self.DATE_INPUT).get_attribute("value")

    def get_error_message(self):
        self.wait.until(lambda d: self.find(self.ERROR_MESSAGE).text.strip() != "")
        return self.find(self.ERROR_MESSAGE).text

    def get_current_month_year(self):
        month = self.find(self.MONTH_BUTTON).text
        year = self.find(self.YEAR_BUTTON).text
        return month, year

    def select_month(self, month_name):
        """Открыть список месяцев и выбрать нужный, например 'January'."""
        self.click(self.MONTH_BUTTON)
        items = self.find_all(self.MONTH_ITEMS)
        for item in items:
            if item.text == month_name:
                item.click()
                return
        raise ValueError(f"Месяц {month_name} не найден в списке")

    def open_year_picker(self):
        self.click(self.YEAR_BUTTON)
        