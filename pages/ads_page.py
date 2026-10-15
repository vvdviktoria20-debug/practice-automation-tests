import time

import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage

# Задержка автопоказа рекламы из настроек попапа (auto_open, delay = 4500 мс).
AD_DELAY_MS = 4500


class AdsPage(BasePage):
    """Страница https://practice-automation.com/ads/

    Реклама открывается САМА через 4.5 секунды после загрузки страницы —
    кнопки для её открытия на странице нет.
    """

    URL = "https://practice-automation.com/ads/"

    AD_OVERLAY = (By.ID, "pum-1272")
    AD_OVERLAY_ACTIVE = (By.CSS_SELECTOR, "#pum-1272.pum-active")
    AD_TITLE = (By.CSS_SELECTOR, "#pum-1272 .pum-title")
    AD_CONTENT = (By.CSS_SELECTOR, "#pum-1272 .pum-content")
    AD_CLOSE_BUTTON = (By.CSS_SELECTOR, "#pum-1272 .pum-close")

    LEARN_MORE_LINK = (By.LINK_TEXT, "Learn More")

    # JS: за один вызов (атомарно) вернуть «сколько мс прошло с начала навигации»
    # и «видна ли реклама». Так время и состояние берутся в один и тот же момент.
    _AD_STATE_JS = """
        const el = document.getElementById('pum-1272');
        let visible = false;
        if (el && el.classList.contains('pum-active')) {
            const s = getComputedStyle(el);
            const r = el.getBoundingClientRect();
            visible = s.display !== 'none' && s.visibility !== 'hidden'
                      && r.width > 0 && r.height > 0;
        }
        return [performance.now(), visible];
    """

    @allure.step("Открыть страницу Ads")
    def open(self):
        self.driver.get(self.URL)

    @allure.step("Дождаться появления рекламного окна")
    def wait_for_ad_to_appear(self):
        self.wait.until(EC.visibility_of_element_located(self.AD_OVERLAY_ACTIVE))

    def is_ad_visible(self):
        overlays = self.driver.find_elements(*self.AD_OVERLAY_ACTIVE)
        return len(overlays) > 0 and overlays[0].is_displayed()

    def get_ad_state(self):
        """Вернуть (мс с начала навигации, видна ли реклама) одним атомарным запросом."""
        elapsed_ms, visible = self.driver.execute_script(self._AD_STATE_JS)
        return elapsed_ms, visible

    @allure.step("Измерить, через сколько мс после начала загрузки появилась реклама")
    def measure_ad_appearance_ms(self, timeout=30):
        """Опрашивать страницу каждые 50 мс и вернуть время (мс от начала навигации),
        в которое реклама впервые оказалась видимой. Не зависит от скорости загрузки:
        отсчёт идёт от начала навигации браузера, а не от момента вызова в тесте."""
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            elapsed_ms, visible = self.get_ad_state()
            if visible:
                return elapsed_ms
            time.sleep(0.05)
        raise TimeoutError("Реклама не появилась за отведённое время")

    @allure.step("Прочитать заголовок рекламы")
    def get_ad_title(self):
        self.wait.until(lambda d: self.find(self.AD_TITLE).text.strip() != "")
        return self.find(self.AD_TITLE).text

    @allure.step("Прочитать текст рекламы")
    def get_ad_text(self):
        self.wait.until(lambda d: self.find(self.AD_CONTENT).text.strip() != "")
        return self.find(self.AD_CONTENT).text

    @allure.step("Закрыть рекламу кнопкой ×")
    def close_ad(self):
        self.click(self.AD_CLOSE_BUTTON)
        self.wait.until(EC.invisibility_of_element_located(self.AD_OVERLAY_ACTIVE))

    @allure.step("Кликнуть мышью по затемнённому фону за пределами окна рекламы")
    def click_overlay_background(self):
        """Настоящий клик мыши (ActionChains) в левый верхний угол оверлея —
        далеко от окна рекламы, которое расположено по центру."""
        overlay = self.find(self.AD_OVERLAY)
        rect = self.driver.execute_script(
            "const r = arguments[0].getBoundingClientRect();"
            "return {left: r.left, top: r.top, width: r.width, height: r.height};",
            overlay,
        )
        x, y = rect["left"] + 10, rect["top"] + 10

        # Убеждаемся, что в этой точке действительно сам оверлей, а не окно рекламы
        # или другой элемент: иначе тест проверял бы не то.
        target_id = self.driver.execute_script(
            "const e = document.elementFromPoint(arguments[0], arguments[1]);"
            "return e ? e.id : null;", x, y)
        assert target_id == "pum-1272", f"В точке клика не оверлей, а элемент id={target_id!r}"

        # В Selenium 4 смещение отсчитывается от центра элемента.
        offset_x = int(x - (rect["left"] + rect["width"] / 2))
        offset_y = int(y - (rect["top"] + rect["height"] / 2))
        ActionChains(self.driver).move_to_element_with_offset(
            overlay, offset_x, offset_y).click().perform()

    @allure.step("Нажать клавишу Escape")
    def press_escape(self):
        ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()

    @allure.step("Убедиться, что реклама остаётся видимой в течение {seconds} с")
    def ad_stays_visible(self, seconds=1.5):
        """True, если реклама ни разу не пропала за seconds секунд (проверка каждые 100 мс)."""
        end = time.monotonic() + seconds
        while time.monotonic() < end:
            if not self.is_ad_visible():
                return False
            time.sleep(0.1)
        return self.is_ad_visible()

    def get_page_text(self):
        return self.driver.find_element(By.TAG_NAME, "body").text

    def get_page_title(self):
        return self.driver.title

    @allure.step("Дождаться заголовка вкладки со словом «{text}»")
    def wait_for_title_containing(self, text):
        """Заголовок вкладки сайт выставляет скриптом уже после загрузки,
        поэтому ждём его, а не читаем сразу. Возвращает реальный заголовок."""
        try:
            self.wait.until(EC.title_contains(text))
        except TimeoutException:
            pass
        return self.driver.title
