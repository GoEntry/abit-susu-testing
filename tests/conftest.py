from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager
import pytest
from classes.config import Config
from pathlib import Path
from datetime import datetime

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()

    if Config.headless():
        options.add_argument("--headless")

    options.add_experimental_option('prefs', {
        'intl.accept_languages': 'ru',
    })

    service = ChromeService(ChromeDriverManager(cache_manager=DriverCacheManager(valid_range=30)).install())

    driver = webdriver.Chrome(options, service)

    window_size = Config.window_size()

    if len(window_size) == 2:
        driver.set_window_size(window_size[0], window_size[1])
    else:
        driver.maximize_window()

    yield driver

    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get('driver')
        if driver:
            screenshots_dir = Path(__file__).parent.parent / "screenshots"
            screenshots_dir.mkdir(exist_ok=True)

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            test_name = item.nodeid.replace("::", "_").replace("/", "_").replace("\\", "_")
            screenshot_path = screenshots_dir / f"{test_name}_{timestamp}.png"

            driver.save_screenshot(str(screenshot_path))
            print(f"\nСкриншот сохранён: {screenshot_path}")
