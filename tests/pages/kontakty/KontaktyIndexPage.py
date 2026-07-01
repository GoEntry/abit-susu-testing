from pages.base.user.page import UserPage

class KontaktyIndexPage(UserPage):
    def open(self):
        super().open("/kontakty/")

    def assert_h1(self):
        super().assert_h1("Контакты")
