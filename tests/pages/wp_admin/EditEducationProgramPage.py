from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base.admin.page import AdminPage


class EditEducationProgramPage(AdminPage):
    def open_by_title(self, title: str):
        """Открывает страницу редактирования программы по её заголовку"""
        # Сначала открываем список программ
        super().open("/wp-admin/edit.php?post_type=education-program")
        
        # Ищем строку с нужной программой и кликаем по ссылке редактирования
        edit_link = self.driver.find_element(
            By.XPATH,
            f"//a[@class='row-title'][{self.text_predicate(title)}]"
        )
        edit_link.click()
        
        # Ждём загрузки страницы редактирования
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "title"))
        )
    
    def update_title(self, new_title: str):
        """Обновляет заголовок программы"""
        title_field = self.driver.find_element(By.ID, "title")
        title_field.clear()
        title_field.send_keys(new_title)
    
    def update_duration(self, new_duration: str):
        """Обновляет срок обучения"""
        duration_field = self.driver.find_element(By.ID, "meta-box-edu-time")
        duration_field.clear()
        duration_field.send_keys(new_duration)
    
    def update_cost(self, new_cost: str):
        """Обновляет стоимость обучения"""
        cost_select = self.driver.find_element(By.NAME, "extra[edu-cost]")
        Select(cost_select).select_by_visible_text(new_cost)
    
    def update_funded_places(self, new_places: str):
        """Обновляет количество бюджетных мест"""
        places_field = self.driver.find_element(By.ID, "meta-box-funded-places")
        places_field.clear()
        places_field.send_keys(new_places)
    
    def update_paid_places(self, new_places: str):
        """Обновляет количество платных мест"""
        places_field = self.driver.find_element(By.ID, "meta-box-paid-places")
        places_field.clear()
        places_field.send_keys(new_places)
    
    def update_passing_score_budget(self, new_score: str):
        """Обновляет проходной балл (бюджет)"""
        score_field = self.driver.find_element(By.ID, "meta-box-passing_score_budget")
        score_field.clear()
        score_field.send_keys(new_score)
    
    def update_passing_score_contract(self, new_score: str):
        """Обновляет проходной балл (контракт)"""
        score_field = self.driver.find_element(By.ID, "meta-box-passing_score_contract")
        score_field.clear()
        score_field.send_keys(new_score)
    
    def update_edu_form(self, new_form: str):
        """Обновляет форму обучения (очная, заочная, очно-заочная)
        
        Args:
            new_form: Форма обучения (например, "очная", "заочная", "очно-заочная")
        """
        from components.fields.select2 import Select2Field
        Select2Field(self.driver, "extra[edu-form]", new_form).handle()
    
    def update_division(self, new_division: str):
        """Обновляет подразделение программы
        
        Args:
            new_division: Название подразделения (например, "Высшая школа экономики и управления")
        """
        from components.fields.select2 import Select2Field
        Select2Field(self.driver, "extra[division]", new_division).handle()
    
    def publish(self, timeout: int = 15):
        """Сохраняет изменения (публикует или обновляет)"""
        # Ищем кнопку "Обновить" или "Опубликовать"
        update_buttons = self.driver.find_elements(By.ID, "publish")
        
        if update_buttons:
            button = update_buttons[0]
            button.click()
            WebDriverWait(self.driver, timeout).until(EC.staleness_of(button))
    
    def get_success_message(self) -> str:
        """Получает сообщение об успешном сохранении"""
        message_elements = self.driver.find_elements(
            By.CSS_SELECTOR, 
            ".notice-success, .updated"
        )
        
        if message_elements:
            return message_elements[0].text
        return ""
    
    def get_slug(self) -> str:
        """Получает slug программы из поля на странице редактирования"""
        slug_field = self.driver.find_element(By.ID, "post_name")
        return slug_field.get_attribute("value")
