from selenium.webdriver.common.by import By
from pages.base.page import Page

class AdminPage(Page):
    def open_menu_pages(self):
        menu = self.driver.find_element(By.ID, "headerMenuCollapse")
        link = menu.find_element(By.LINK_TEXT, "Страницы")
        link.click()
