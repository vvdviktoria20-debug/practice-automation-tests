import allure
from pages.modals_page import ModalsPage


@allure.epic("Modals")
class TestModals:

    # ---------- Позитивные тесты ----------

    @allure.title("Открытие простого модального окна")
    def test_open_simple_modal(self, driver):
        page = ModalsPage(driver)
        page.open()
        page.open_simple_modal()
        assert page.is_modal_open()

    @allure.title("Текст простого модального окна корректен")
    def test_simple_modal_text(self, driver):
        page = ModalsPage(driver)
        page.open()
        page.open_simple_modal()
        assert "simple modal" in page.get_modal_text().lower()

    @allure.title("Закрытие простого модального окна")
    def test_close_simple_modal(self, driver):
        page = ModalsPage(driver)
        page.open()
        page.open_simple_modal()
        page.close_modal()
        assert not page.is_modal_open()

    @allure.title("Открытие модального окна с формой")
    def test_open_form_modal(self, driver):
        page = ModalsPage(driver)
        page.open()
        page.open_form_modal()
        assert page.is_modal_open()
        assert page.find(page.NAME_INPUT).is_displayed()

    @allure.title("Закрытие модального окна с формой")
    def test_close_form_modal(self, driver):
        page = ModalsPage(driver)
        page.open()
        page.open_form_modal()
        page.close_modal()
        assert not page.is_modal_open()

    @allure.title("Повторное открытие простого модального окна")
    def test_reopen_simple_modal(self, driver):
        page = ModalsPage(driver)
        page.open()
        page.open_simple_modal()
        page.close_modal()
        page.open_simple_modal()
        assert page.is_modal_open()

    @allure.title("Отправка формы с валидными данными")
    def test_submit_form_valid_data(self, driver):
        page = ModalsPage(driver)
        page.open()
        page.open_form_modal()
        page.fill_form(name="Ivan Ivanov", email="ivan@test.com", message="Test message")
        page.submit_form()
        assert "thank you" in page.get_page_text().lower()

    # ---------- Негативные тесты ----------

    @allure.title("Форма отправляется даже с пустым полем Name (валидация отсутствует)")
    def test_submit_form_empty_name(self, driver):
        page = ModalsPage(driver)
        page.open()
        page.open_form_modal()
        page.fill_form(email="ivan@test.com", message="Test message")
        page.submit_form()
        assert "thank you" in page.get_page_text().lower()

    @allure.title("Форма отправляется даже с некорректным Email (валидация отсутствует)")
    def test_submit_form_invalid_email(self, driver):
        page = ModalsPage(driver)
        page.open()
        page.open_form_modal()
        page.fill_form(name="Ivan Ivanov", email="ivan@@test", message="Test message")
        page.submit_form()
        assert "thank you" in page.get_page_text().lower()

    @allure.title("Форма отправляется даже со всеми пустыми полями (валидация отсутствует)")
    def test_submit_form_all_empty(self, driver):
        page = ModalsPage(driver)
        page.open()
        page.open_form_modal()
        page.submit_form()
        assert "thank you" in page.get_page_text().lower()