from pages.base.admin.page import AdminPage

class EducationProgramListPage(AdminPage):
    def open(self):
        super().open("/wp-admin/edit.php?post_type=education-program")

    def assert_empty(self, timeout: int = 5):
        xpath = f"//tr[{self.text_predicate('Не найдены Образовательные программы')}]"
        self.assert_visible_text(xpath, timeout)

    def assert_contains(self, title: str, timeout: int = 5):
        xpath = f"//tr[{self.text_predicate(title)}]"
        self.assert_visible_text(xpath, timeout)
