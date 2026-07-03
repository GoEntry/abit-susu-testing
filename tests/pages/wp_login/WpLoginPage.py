from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base.admin.page import AdminPage

class WpLoginPage(AdminPage):
    def open(self):
        super().open("/wp-login.php")

    def login(self, username: str, password: str, timeout: int = 10):
        self.driver.find_element(By.ID, "user_login").send_keys(username)
        self.driver.find_element(By.ID, "user_pass").send_keys(password)
        self.driver.find_element(By.ID, "wp-submit").click()
        # Клик запускает переход по редиректу логина; если сразу открыть
        # следующую страницу, эта навигация может оборваться раньше, чем
        # успеет выставиться cookie сессии, и пользователь останется
        # неавторизованным без единой ошибки. Ждём админ-бар как подтверждение
        # завершённого входа перед тем, как продолжать сценарий.
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.ID, "wpadminbar"))
        )
