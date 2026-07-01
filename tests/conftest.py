from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import pytest
from classes.config import Config

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()

    if Config.headless():
        options.add_argument("--headless")

    options.add_experimental_option('prefs', {
        'intl.accept_languages': 'ru',
    })

    service = ChromeService(ChromeDriverManager().install())

    driver = webdriver.Chrome(options, service)

    window_size = Config.window_size()

    if len(window_size) == 2:
        driver.set_window_size(window_size[0], window_size[1])
    else:
        driver.maximize_window()

    yield driver

    driver.quit()
