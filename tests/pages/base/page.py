import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver

class Page():
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def get_app_url(self) -> str:
        return os.environ.get("SITE_URL")

    def open(self, path: str):
        self.driver.get(self.get_app_url()+path)

    @staticmethod
    def text_predicate(text: str) -> str:
        # &nbsp; (U+00A0) renders as a regular space but is a distinct
        # character in the DOM text node, so contains() must normalize it.
        return f"contains(translate(., ' ', ' '), '{text}')"

    def assert_visible_text(self, xpath: str, timeout: int = 5):
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )

    def assert_tag_text(self, tag: str, text: str, timeout: int = 1):
        self.assert_visible_text(f"//{tag}[{self.text_predicate(text)}]", timeout)

    def assert_h1(self, text: str, timeout: int = 1):
        self.assert_tag_text("h1", text, timeout)

    def assert_h2(self, text: str, timeout: int = 1):
        self.assert_tag_text("h2", text, timeout)

    def assert_h3(self, text: str, timeout: int = 1):
        self.assert_tag_text("h3", text, timeout)

    def assert_span(self, text: str, timeout: int = 1):
        self.assert_tag_text("span", text, timeout)

