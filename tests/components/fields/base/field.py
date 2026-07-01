import time
from dataclasses import dataclass
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement

@dataclass
class Field:
    driver: WebDriver

    def scroll_to_element(self, by: By, name: str) -> WebElement:
        element = WebDriverWait(self.driver, 1).until(
            EC.presence_of_element_located((by, name))
        )
        top = element.location["y"]

        self.driver.execute_script("window.scrollTo(0, "+str(top)+");")
        time.sleep(1)

        return element
