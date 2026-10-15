import allure

from pages.modals_page import ModalsPage

SUCCESS_TEXT = "thank you for your response"


@allure.epic("Practice Automation")
@allure.feature("Modals")
class TestModals:

    # ---------- ПОЗИТИВНЫЕ ТЕСТЫ ----------

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

    @allure.title("Модальное окно с формой содержит поля Name, Email, Message и кнопку Submit")
    def test_open_form_modal(self, driver):
        page = ModalsPage(driver)
        page.open()
        page.open_form_modal()
        assert page.is_modal_open()
        assert page.find(page.NAME_INPUT).is_displayed(), "Поле Name не отображается"
        assert page.find(page.EMAIL_INPUT).is_displayed(), "Поле Email не отображается"
        assert page.find(page.MESSAGE_INPUT).is_displayed(), "Поле Message не отображается"
        assert page.find(page.SUBMIT_BUTTON).is_displayed(), "Кнопка Submit не отображается"

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
        assert "simple modal" in page.get_modal_text().lower()

    @allure.title("Отправка формы с валидными данными")
    def test_submit_form_valid_data(self, driver):
        page = ModalsPage(driver)
        page.open()
        page.open_form_modal()
        page.fill_form(name="Ivan Ivanov", email="ivan@test.com", message="Test message")
        page.submit_form()
        assert SUCCESS_TEXT in page.get_success_message().lower()

    # ---------- НЕГАТИВНЫЕ ТЕСТЫ ----------
    # У формы на сайте нет клиентской валидации, поэтому «некорректные» данные
    # всё равно принимаются. Тесты фиксируют это реальное поведение.

    @allure.title("Форма отправляется даже с пустым полем Name (валидации нет)")
    def test_submit_form_empty_name(self, driver):
        page = ModalsPage(driver)
        page.open()
        page.open_form_modal()
        page.fill_form(email="ivan@test.com", message="Test message")
        page.submit_form()
        assert SUCCESS_TEXT in page.get_success_message().lower()

    @allure.title("Форма отправляется даже с некорректным Email (валидации нет)")
    def test_submit_form_invalid_email(self, driver):
        page = ModalsPage(driver)
        page.open()
        page.open_form_modal()
        page.fill_form(name="Ivan Ivanov", email="ivan@@test", message="Test message")
        page.submit_form()
        assert SUCCESS_TEXT in page.get_success_message().lower()

    @allure.title("Форма отправляется даже со всеми пустыми полями (валидации нет)")
    def test_submit_form_all_empty(self, driver):
        page = ModalsPage(driver)
        page.open()
        page.open_form_modal()
        page.submit_form()
        assert SUCCESS_TEXT in page.get_success_message().lower()
