from selenium.webdriver.common.by import By
from pages.base.user.page import UserPage

class ResetDbPage(UserPage):
    RESET_DB_XPATH = "//label[@for='reset-db']"

    def open(self):
        super().open("/test/")

    def assert_reset_db_button_visible(self, timeout: int = 5):
        self.assert_visible_text(self.RESET_DB_XPATH, timeout)

    def click_reset_db(self):
        self.driver.find_element(By.XPATH, self.RESET_DB_XPATH).click()
