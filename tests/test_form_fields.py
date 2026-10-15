import allure

from pages.form_fields_page import FormFieldsPage


@allure.epic("Practice Automation")
@allure.feature("Form Fields: Automation tools → Message")
class TestFormFieldsAutomationTools:

    @allure.title("В блоке «Automation tools» есть элементы, среди них Selenium")
    def test_automation_tools_list_is_not_empty(self, driver):
        page = FormFieldsPage(driver)
        page.open()
        tools = page.get_automation_tools()
        assert len(tools) > 0, "Список Automation tools пуст"
        assert "Selenium" in tools, f"Selenium не найден в списке: {tools}"

    @allure.title("Поле Message заполняется списком Automation tools через запятую")
    def test_fill_message_with_automation_tools(self, driver):
        page = FormFieldsPage(driver)
        page.open()
        tools, expected_text = page.fill_message_with_automation_tools()
        allure.attach(expected_text, name="Текст, записанный в Message",
                      attachment_type=allure.attachment_type.TEXT)
        actual = page.get_message_value()
        assert actual == expected_text
        assert actual.split(", ") == tools
