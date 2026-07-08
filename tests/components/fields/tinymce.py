from dataclasses import dataclass
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from components.fields.base.field import Field


@dataclass
class TinymceField(Field):
    frame: str
    value: str

    def handle(self):
        WebDriverWait(self.driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, self.frame))
        )

        body = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        body.click()

        self.driver.execute_script(
            "arguments[0].innerHTML = arguments[1];",
            body,
            self.value
        )

        self.driver.switch_to.default_content()
