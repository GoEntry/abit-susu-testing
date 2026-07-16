from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base.user.page import UserPage

class ResetDbPage(UserPage):
    RESET_DB_XPATH = "//label[@for='reset-db']"
    SUCCESS_MESSAGE_XPATH = "//*[contains(text(), 'База данных сброшена')]"

    def open(self):
        super().open("/test/")

    def assert_reset_db_button_visible(self, timeout: int = 5):
        self.assert_visible_text(self.RESET_DB_XPATH, timeout)

    def click_reset_db(self):
        self.driver.find_element(By.XPATH, self.RESET_DB_XPATH).click()

    def assert_success_message_visible(self, timeout: int = 5):
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((By.XPATH, self.SUCCESS_MESSAGE_XPATH))
        )
