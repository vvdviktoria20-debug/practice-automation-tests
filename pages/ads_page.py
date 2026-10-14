from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class AdsPage(BasePage):
    URL = "https://practice-automation.com/ads/"

    # Реклама открывается САМА через 4.5 секунды после загрузки страницы —
    # кнопки для её открытия на странице нет.
    AD_OVERLAY = (By.ID, "pum-1272")
    AD_OVERLAY_ACTIVE = (By.CSS_SELECTOR, "#pum-1272.pum-active")
    AD_TITLE = (By.CSS_SELECTOR, "#pum-1272 .pum-title")
    AD_CONTENT = (By.CSS_SELECTOR, "#pum-1272 .pum-content")
    AD_CLOSE_BUTTON = (By.CSS_SELECTOR, "#pum-1272 .pum-close")

    LEARN_MORE_LINK = (By.LINK_TEXT, "Learn More")

    def open(self):
        self.driver.get(self.URL)

    def wait_for_ad_to_appear(self):
        self.wait.until(EC.visibility_of_element_located(self.AD_OVERLAY_ACTIVE))

    def is_ad_visible(self):
        overlays = self.driver.find_elements(*self.AD_OVERLAY_ACTIVE)
        return len(overlays) > 0 and overlays[0].is_displayed()

    def get_ad_title(self):
        self.wait.until(lambda d: self.find(self.AD_TITLE).text.strip() != "")
        return self.find(self.AD_TITLE).text

    def get_ad_text(self):
        self.wait.until(lambda d: self.find(self.AD_CONTENT).text.strip() != "")
        return self.find(self.AD_CONTENT).text

    def close_ad(self):
        self.click(self.AD_CLOSE_BUTTON)
        self.wait.until(EC.invisibility_of_element_located(self.AD_OVERLAY_ACTIVE))

    def click_overlay_background(self):
        # Кликаем именно по фону (overlay), а не по содержимому попапа,
        # через JS — чтобы клик пришёлся точно на сам overlay-элемент.
        overlay = self.find(self.AD_OVERLAY)
        self.driver.execute_script("arguments[0].click();", overlay)

    def press_escape(self):
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)

    def get_page_text(self):
        return self.driver.find_element(By.TAG_NAME, "body").text

    def get_page_title(self):
        return self.driver.title