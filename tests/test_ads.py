import time

import allure

from pages.ads_page import AdsPage


@allure.epic("Practice Automation")
@allure.feature("Ads")
class TestAds:

    # ---------- ПОЗИТИВНЫЕ ТЕСТЫ ----------

    @allure.title("Страница Ads открывается и имеет правильный заголовок")
    def test_open_ads_page(self, driver):
        page = AdsPage(driver)
        page.open()
        assert "Ads" in page.get_page_title()

    @allure.title("Реклама появляется автоматически после задержки")
    def test_ad_appears_automatically(self, driver):
        page = AdsPage(driver)
        page.open()
        page.wait_for_ad_to_appear()
        assert page.is_ad_visible() is True

    @allure.title("У рекламного окна корректный заголовок")
    def test_ad_title_text(self, driver):
        page = AdsPage(driver)
        page.open()
        page.wait_for_ad_to_appear()
        assert page.get_ad_title().strip().lower() == "hi"

    @allure.title("У рекламного окна корректный текст")
    def test_ad_content_text(self, driver):
        page = AdsPage(driver)
        page.open()
        page.wait_for_ad_to_appear()
        assert "i am an ad" in page.get_ad_text().lower()

    @allure.title("Рекламное окно закрывается по кнопке ×")
    def test_close_ad_with_close_button(self, driver):
        page = AdsPage(driver)
        page.open()
        page.wait_for_ad_to_appear()
        page.close_ad()
        assert page.is_ad_visible() is False

    @allure.title("На странице есть предупреждение про блокировщики рекламы")
    def test_page_contains_adblock_warning(self, driver):
        page = AdsPage(driver)
        page.open()
        assert "ad blockers are turned off" in page.get_page_text().lower()

    @allure.title("На странице есть текст с обратным отсчётом")
    def test_page_contains_countdown_text(self, driver):
        page = AdsPage(driver)
        page.open()
        assert "an ad will appear" in page.get_page_text().lower()

    @allure.title("На странице есть ссылка 'Learn More'")
    def test_page_contains_learn_more_link(self, driver):
        page = AdsPage(driver)
        page.open()
        link = page.find(page.LEARN_MORE_LINK)
        assert link.get_attribute("href") == "https://linktr.ee/automateNow"

    # ---------- НЕГАТИВНЫЕ ТЕСТЫ ----------

    @allure.title("Реклама НЕ появляется сразу после загрузки страницы (есть задержка)")
    def test_ad_not_visible_immediately(self, driver):
        page = AdsPage(driver)
        page.open()
        assert page.is_ad_visible() is False

    @allure.title("Клик по фону (overlay) НЕ закрывает рекламное окно")
    def test_clicking_overlay_does_not_close_ad(self, driver):
        page = AdsPage(driver)
        page.open()
        page.wait_for_ad_to_appear()
        page.click_overlay_background()
        time.sleep(0.5)
        assert page.is_ad_visible() is True

    @allure.title("Нажатие Escape НЕ закрывает рекламное окно")
    def test_pressing_escape_does_not_close_ad(self, driver):
        page = AdsPage(driver)
        page.open()
        page.wait_for_ad_to_appear()
        page.press_escape()
        time.sleep(0.5)
        assert page.is_ad_visible() is True