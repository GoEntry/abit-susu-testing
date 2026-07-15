from dataclasses import dataclass
from typing import Union
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from components.fields.base.field import Field
import time


@dataclass
class Select2Field(Field):
    name: str
    values: Union[str, list]

    def handle(self, wait_after_select = False):
        for text in self._as_list(self.values):
            self._widget().click()
            self._option(text).click()
            self._wait_dropdown_closed()
            if wait_after_select:
                time.sleep(1)

    def _as_list(self, values) -> list:
        return values if isinstance(values, list) else [values]

    def _wait_dropdown_closed(self):
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, ".select2-dropdown"))
        )

    def _widget(self):
        base = f'select[name="{self.name}"] + span'

        has_search_field = self.driver.find_elements(By.CSS_SELECTOR, f"{base} .select2-search__field")
        selector = f"{base} .select2-search__field" if has_search_field else f"{base} .select2-selection"
        widget = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
        )

        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", widget)
        return widget

    def _option(self, text: str):
        xpath = f"//li[contains(@class, 'select2-results__option')][text()='{text}']"
        return WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
