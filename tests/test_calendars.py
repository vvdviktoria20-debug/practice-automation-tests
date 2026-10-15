import allure

from pages.calendars_page import CalendarsPage, MONTHS, shift_month


@allure.epic("Practice Automation")
@allure.feature("Calendars")
class TestCalendars:

    # ---------- ПОЗИТИВНЫЕ ТЕСТЫ ----------

    @allure.title("Страница Calendars открывается")
    def test_open_calendars_page(self, driver):
        page = CalendarsPage(driver)
        page.open()
        assert "practice-automation" in driver.current_url
        assert page.find(page.DATE_INPUT).is_displayed()

    @allure.title("Стрелка «вперёд» переключает на следующий месяц")
    def test_next_month_arrow(self, driver):
        page = CalendarsPage(driver)
        page.open()
        page.open_datepicker()
        month, year = page.get_current_month_year()
        page.click_next_month()
        expected = shift_month(month, year, +1)
        assert page.wait_for_month_year(expected) == expected

    @allure.title("Стрелка «назад» переключает на предыдущий месяц")
    def test_prev_month_arrow(self, driver):
        page = CalendarsPage(driver)
        page.open()
        page.open_datepicker()
        month, year = page.get_current_month_year()
        page.click_prev_month()
        expected = shift_month(month, year, -1)
        assert page.wait_for_month_year(expected) == expected

    @allure.title("Переход «вперёд» из декабря ведёт в январь следующего года")
    def test_next_arrow_from_december_goes_to_january_next_year(self, driver):
        page = CalendarsPage(driver)
        page.open()
        page.open_datepicker()
        page.select_month("December")
        _, year = page.get_current_month_year()
        page.click_next_month()
        expected = ("January", str(int(year) + 1))
        assert page.wait_for_month_year(expected) == expected

    @allure.title("Переход «назад» из января ведёт в декабрь предыдущего года")
    def test_prev_arrow_from_january_goes_to_december_previous_year(self, driver):
        page = CalendarsPage(driver)
        page.open()
        page.open_datepicker()
        page.select_month("January")
        _, year = page.get_current_month_year()
        page.click_prev_month()
        expected = ("December", str(int(year) - 1))
        assert page.wait_for_month_year(expected) == expected

    @allure.title("Выбор месяца из списка")
    def test_select_month(self, driver):
        page = CalendarsPage(driver)
        page.open()
        page.open_datepicker()
        _, year = page.get_current_month_year()
        page.select_month("March")
        expected = ("March", year)
        assert page.wait_for_month_year(expected) == expected

    @allure.title("Выбор даты кликом на число: в поле полная дата YYYY-MM-DD")
    def test_click_day(self, driver):
        page = CalendarsPage(driver)
        page.open()
        page.open_datepicker()
        month, year = page.get_current_month_year()
        page.click_day(15)
        expected = f"{year}-{MONTHS.index(month) + 1:02d}-15"
        assert page.wait_for_input_value(expected) == expected

    @allure.title("Выбор даты через переход на 3 месяца вперёд: полная дата верна")
    def test_select_date_with_pagination(self, driver):
        page = CalendarsPage(driver)
        page.open()
        page.open_datepicker()
        month, year = page.get_current_month_year()
        for _ in range(3):
            page.click_next_month()
        exp_month, exp_year = shift_month(month, year, +3)
        assert page.wait_for_month_year((exp_month, exp_year)) == (exp_month, exp_year)
        page.click_day(10)
        expected = f"{exp_year}-{MONTHS.index(exp_month) + 1:02d}-10"
        assert page.wait_for_input_value(expected) == expected

    @allure.title("Выбор минимального года 1926")
    def test_select_min_year(self, driver):
        page = CalendarsPage(driver)
        page.open()
        page.open_datepicker()
        page.select_year(1926)
        assert page.wait_for_year(1926) == "1926"

    @allure.title("Выбор максимального года 2126")
    def test_select_max_year(self, driver):
        page = CalendarsPage(driver)
        page.open()
        page.open_datepicker()
        page.select_year(2126)
        assert page.wait_for_year(2126) == "2126"

    # ---------- НЕГАТИВНЫЕ ТЕСТЫ ----------

    @allure.title("Произвольный текст показывает ошибку «valid date»")
    def test_invalid_text_shows_error(self, driver):
        page = CalendarsPage(driver)
        page.open()
        page.type_date("hello")
        page.blur_date_input()
        assert "valid date" in page.get_error_message().lower()

    @allure.title("Несуществующая дата 2026-13-35 показывает ошибку")
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
