import os

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="session")
def chromedriver_path():
    """Находим/скачиваем ChromeDriver ОДИН раз за весь запуск, а не перед каждым тестом
    (раньше проверка версии через интернет повторялась 37 раз — это тормозило и
    на медленной сети роняло тесты). Если не получилось — Selenium найдёт драйвер сам."""
    try:
        return ChromeDriverManager().install()
    except Exception:
        return None


@pytest.fixture
def driver(chromedriver_path):
    """Новый браузер Chrome для каждого теста. Закрывается после теста.

    Запуск без окна (например, на сервере): HEADLESS=1 pytest
    """
    options = Options()
    if os.getenv("HEADLESS") == "1":
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
    service = Service(chromedriver_path) if chromedriver_path else Service()
    driver = webdriver.Chrome(service=service, options=options)
    if os.getenv("HEADLESS") != "1":
        driver.maximize_window()
    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Если тест упал — сохраняем скриншот и прикладываем его к Allure-отчёту."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver is not None:
            os.makedirs("screenshots", exist_ok=True)
            driver.save_screenshot(f"screenshots/{item.name}.png")

            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot-on-failure",
                attachment_type=allure.attachment_type.PNG,
            )
