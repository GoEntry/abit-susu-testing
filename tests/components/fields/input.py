from dataclasses import dataclass
from typing import Union
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from components.fields.base.field import Field

@dataclass
class InputField(Field):
    by: By
    name: str
    value: Union[str, int]

    def handle(self):
        field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((self.by, self.name))
        )
        field.send_keys(self.value)
