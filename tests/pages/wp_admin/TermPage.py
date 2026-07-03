from selenium.webdriver.common.by import By
from pages.base.admin.page import AdminPage

class TermPage(AdminPage):
    def open(self, taxonomy: str):
        super().open(f"/wp-admin/edit-tags.php?taxonomy={taxonomy}&post_type=education-program")

    def add_term(self, name: str, timeout: int = 10):
        # Форма отправляется через AJAX (без перезагрузки страницы), поэтому
        # ждём появления термина в таблице, а не просто кликаем и продолжаем.
        self.driver.find_element(By.ID, "tag-name").send_keys(name)
        self.driver.find_element(By.ID, "submit").click()
        self.assert_visible_text(f"//tr[{self.text_predicate(name)}]", timeout)
