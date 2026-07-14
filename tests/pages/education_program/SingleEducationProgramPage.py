from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base.user.page import UserPage


class SingleEducationProgramPage(UserPage):
    """Страница одиночной образовательной программы на фронтенде"""
    
    def open_by_slug(self, slug: str):
        """Открывает страницу программы по слагу"""
        super().open(f"/education-program/{slug}/")
    
    def get_title(self) -> str:
        """Получает заголовок программы"""
        title_selectors = [
            "h1.entry-title",
            "h1.program-title",
            ".edu-program__title h1",
            "h1",
        ]
        
        for selector in title_selectors:
            elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
            if elements:
                return elements[0].text.strip()
        
        return ""
    
    def get_duration(self) -> str:
        """Получает срок обучения со страницы"""
        # Ищем блок с информацией о сроке обучения
        duration_elements = self.driver.find_elements(
            By.XPATH,
            f"//*[{self.text_predicate('Срок обучения')}]/following-sibling::*[1] | "
            f"//*[{self.text_predicate('Продолжительность')}]/following-sibling::*[1] | "
            f"//*[contains(@class, 'duration')]"
        )
        
        if duration_elements:
            return duration_elements[0].text.strip()
        
        return ""
    
    def get_cost(self) -> str:
        """Получает стоимость обучения со страницы"""
        cost_elements = self.driver.find_elements(
            By.XPATH,
            f"//*[{self.text_predicate('Стоимость')}]/following-sibling::*[1] | "
            f"//*[contains(@class, 'cost')] | "
            f"//*[contains(@class, 'price')]"
        )
        
        if cost_elements:
            return cost_elements[0].text.strip()
        
        return ""
    
    def get_funded_places(self) -> str:
        """Получает количество бюджетных мест"""
        places_elements = self.driver.find_elements(
            By.XPATH,
            f"//*[{self.text_predicate('Бюджетных мест')}]/following-sibling::*[1] | "
            f"//*[{self.text_predicate('бюджет')}] | "
            f"//*[contains(@class, 'funded-places')]"
        )
        
        if places_elements:
            return places_elements[0].text.strip()
        
        return ""
    
    def get_passing_score_budget(self) -> str:
        """Получает проходной балл на бюджет"""
        score_elements = self.driver.find_elements(
            By.XPATH,
            f"//*[{self.text_predicate('Проходной балл')}]/following-sibling::*[1] | "
            f"//*[contains(@class, 'passing-score-budget')]"
        )
        
        if score_elements:
            return score_elements[0].text.strip()
        
        return ""
    
    def assert_contains_text(self, text: str, timeout: int = 10):
        """Проверяет наличие текста на странице"""
        self.assert_visible_text(
            f"//*[{self.text_predicate(text)}]",
            timeout
        )
