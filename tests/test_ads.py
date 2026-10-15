import allure

from pages.ads_page import AdsPage, AD_DELAY_MS


@allure.epic("Practice Automation")
@allure.feature("Ads")
class TestAds:

    # ---------- ПОЗИТИВНЫЕ ТЕСТЫ ----------

    @allure.title("Страница Ads открывается и имеет правильный заголовок вкладки")
    def test_open_ads_page(self, driver):
        page = AdsPage(driver)
        page.open()
        assert "/ads" in driver.current_url
        assert "Ads" in page.wait_for_title_containing("Ads")

    @allure.title("Реклама появляется автоматически, без кликов пользователя")
    def test_ad_appears_automatically(self, driver):
        page = AdsPage(driver)
        page.open()
        page.wait_for_ad_to_appear()
        assert page.is_ad_visible() is True

    @allure.title("Реклама появляется через настроенную задержку 4.5 с (от начала загрузки)")
    def test_ad_appears_after_configured_delay(self, driver):
        page = AdsPage(driver)
        page.open()
        appeared_at_ms = page.measure_ad_appearance_ms()
        # Не раньше задержки; верхняя граница с запасом на загрузку страницы и опрос.
        assert appeared_at_ms >= AD_DELAY_MS, (
            f"Реклама появилась через {appeared_at_ms:.0f} мс, ожидалось не раньше {AD_DELAY_MS} мс"
        )

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

    @allure.title("На странице есть текст «An ad will appear…»")
    def test_page_contains_countdown_text(self, driver):
        page = AdsPage(driver)
        page.open()
        assert "an ad will appear" in page.get_page_text().lower()

    @allure.title("Ссылка «Learn More» ведёт на linktr.ee/automateNow")
    def test_page_contains_learn_more_link(self, driver):
        page = AdsPage(driver)
        page.open()
        link = page.find(page.LEARN_MORE_LINK)
        assert link.get_attribute("href") == "https://linktr.ee/automateNow"

    # ---------- НЕГАТИВНЫЕ ТЕСТЫ ----------

    @allure.title("Реклама НЕ видна раньше, чем истекла задержка 4.5 с")
    def test_ad_not_visible_before_delay(self, driver):
        page = AdsPage(driver)
        page.open()
        # Время и видимость берутся одним атомарным запросом, поэтому результат
        # не зависит от скорости загрузки страницы: если реклама видна, то
        # с начала навигации обязано пройти не меньше AD_DELAY_MS.
        elapsed_ms, visible = page.get_ad_state()
        assert not visible or elapsed_ms >= AD_DELAY_MS, (
            f"Реклама видна уже через {elapsed_ms:.0f} мс, задержка должна быть {AD_DELAY_MS} мс"
        )

    @allure.title("Клик мышью по фону (overlay) НЕ закрывает рекламу")
    def test_clicking_overlay_does_not_close_ad(self, driver):
        page = AdsPage(driver)
        page.open()
        page.wait_for_ad_to_appear()
        page.click_overlay_background()
        assert page.ad_stays_visible() is True

    @allure.title("Нажатие Escape НЕ закрывает рекламу")
    def test_pressing_escape_does_not_close_ad(self, driver):
        page = AdsPage(driver)
        page.open()
        page.wait_for_ad_to_appear()
        page.press_escape()
        assert page.ad_stays_visible() is True
