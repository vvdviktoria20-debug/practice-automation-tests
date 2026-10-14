import allure
import pytest
from pages.calendars_page import CalendarsPage


@allure.epic("Calendars")
class TestCalendars:

    @allure.title("Открытие страницы Calendars")
    def test_open_calendars_page(self, driver):
        page = CalendarsPage(driver)
        page.open()
        assert "practice-automation" in driver.current_url

    @allure.title("Стрелка 'вперёд' переключает месяц")
    def test_next_month_arrow(self, driver):
        page = CalendarsPage(driver)
        page.open()
        page.open_datepicker()
        before = page.get_current_month_year()
        page.click_next_month()
        after = page.get_current_month_year()
        assert before != after

    @allure.title("Стрелка 'назад' переключает месяц")
    def test_prev_month_arrow(self, driver):
        page = CalendarsPage(driver)
        page.open()
        page.open_datepicker()
        before = page.get_current_month_year()
        page.click_prev_month()
        after = page.get_current_month_year()
        assert before != after

    @allure.title("Выбор месяца из списка")
    def test_select_month(self, driver):
        page = CalendarsPage(driver)
        page.open()
        page.open_datepicker()
        page.select_month("January")
        month, _ = page.get_current_month_year()
        assert month == "January"

    @allure.title("Выбор месяца из списка")
    def test_select_month(self, driver):
        page = CalendarsPage(driver)
        page.open()
        page.open_datepicker()
        page.select_month("January")
        month, _ = page.get_current_month_year()
        assert month == "January"

    @allure.title("Выбор месяца из списка")
    def test_select_month(self, driver):
        page = CalendarsPage(driver)
        page.open()
        page.open_datepicker()
        page.select_month("January")
        month, _ = page.get_current_month_year()
        assert month == "January"

    @allure.title("Выбор даты кликом на число")
    def test_click_day(self, driver):
        page = CalendarsPage(driver)
        page.open()
        page.open_datepicker()
        page.click_day(15)
        assert page.get_input_value().endswith("-15")

    @allure.title("Выбор даты через пагинацию")
    def test_select_date_with_pagination(self, driver):
        page = CalendarsPage(driver)
        page.open()
        page.open_datepicker()
        for _ in range(3):
            page.click_next_month()
        page.click_day(10)
        assert page.get_input_value().endswith("-10")

    @allure.title("Случайный текст показывает ошибку валидации")
    def test_invalid_text_shows_error(self, driver):
        page = CalendarsPage(driver)
        page.open()
        page.type_date("hello")
        page.blur_date_input()
        assert "valid date" in page.get_error_message().lower()

    @allure.title("Несуществующая дата показывает ошибку")
    def test_invalid_date_shows_error(self, driver):
        page = CalendarsPage(driver)
        page.open()
        page.type_date("2026-13-35")
        page.blur_date_input()
        assert "valid date" in page.get_error_message().lower()

    @allure.title("Спецсимволы показывают ошибку")
    def test_special_characters_show_error(self, driver):
        page = CalendarsPage(driver)
        page.open()
        page.type_date("!!!")
        page.blur_date_input()
        assert "valid date" in page.get_error_message().lower()