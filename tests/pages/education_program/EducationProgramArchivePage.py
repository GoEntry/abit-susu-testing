from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base.user.page import UserPage


class EducationProgramArchivePage(UserPage):
    def open(self):
        super().open("/education-program/")

    def assert_has_programs(self, timeout: int = 10):
        """Проверяет, что на странице есть хотя бы одна образовательная программа"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".edu-program__item, .education-program-card, .program-item, article.education-program, .edu-program")
                )
            )
        except Exception as e:
            # Отладка: выводим URL и HTML для диагностики
            print(f"\nТекущий URL: {self.driver.current_url}")
            print(f"\nTitle страницы: {self.driver.title}")

            # Проверяем основной контейнер
            main_containers = self.driver.find_elements(By.CSS_SELECTOR, "main, .main-content, #main, .content")
            print(f"\nНайдено основных контейнеров: {len(main_containers)}")

            # Пытаемся найти любые элементы, которые могут быть карточками программ
            possible_selectors = [
                ".edu-program",
                ".edu-program__item",
                ".education-program-card",
                ".program-item",
                "article.education-program",
                "[class*='program']",
                "[class*='edu']",
            ]

            for selector in possible_selectors:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"\nНайдено {len(elements)} элементов по селектору: {selector}")
                    if elements and len(elements) <= 5:
                        for i, elem in enumerate(elements[:3]):
                            print(f"  Элемент {i+1} classes: {elem.get_attribute('class')}")

            # Выводим часть HTML для анализа
            body_html = self.driver.find_element(By.TAG_NAME, "body").get_attribute("innerHTML")
            print(f"\nПервые 2000 символов body HTML:\n{body_html[:2000]}")

            raise e

    def get_program_count(self) -> int:
        programs = self.driver.find_elements(
            By.CSS_SELECTOR, ".edu-program, .edu-program__item, .education-program-card, .program-item, article.education-program"
        )
        return len(programs)

    def get_program_titles(self) -> list:
        programs = self.driver.find_elements(
            By.CSS_SELECTOR, ".edu-program, .edu-program__item, .education-program-card, .program-item, article.education-program"
        )
        titles = []
        for program in programs:
            title_elements = program.find_elements(By.CSS_SELECTOR, ".title-h3, .program-title, h3, .edu-program__name_title, .edu-program__name .title-h3")
            if title_elements:
                titles.append(title_elements[0].text.strip())

        return titles

    def select_filter_direction(self, direction: str):
        direction_input = self.driver.find_element(By.NAME, "extra[edu-area-name]")

        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", direction_input)

        direction_input.clear()
        direction_input.send_keys(direction)

        import time
        time.sleep(0.5)

        self.driver.execute_script("""
            var element = arguments[0];
            element.dispatchEvent(new Event('change', { bubbles: true }));
            element.dispatchEvent(new Event('blur', { bubbles: true }));
        """, direction_input)

    def select_filter_exam_subjects(self, subjects: list):
        """Выбирает вступительные испытания через select2 (множественный выбор)"""
        from components.fields.select2 import Select2Field

        Select2Field(self.driver, "extra[subjects-ege][]", subjects).handle()


    def select_filter_form(self, form: str):
        """Выбирает форму обучения через обычный select"""
        from selenium.webdriver.support.select import Select

        form_select = self.driver.find_element(By.NAME, "extra[edu-form]")
        Select(form_select).select_by_visible_text(form)

    def select_filter_education_level(self, level: str):
        """Выбирает уровень образования через обычный select"""
        from selenium.webdriver.support.select import Select
        
        possible_names = [
            "extra[education-level]",
            "extra[level]",
            "extra[edu-level]",
            "extra[qualification]",
        ]
        
        for name in possible_names:
            elements = self.driver.find_elements(By.NAME, name)
            if elements:
                Select(elements[0]).select_by_visible_text(level)
                return

    def select_filter_division(self, division: str):
        from selenium.webdriver.support.select import Select
        division_select = self.driver.find_element(By.NAME, "extra[division]")
        Select(division_select).select_by_visible_text(division)

    def click_apply_filters(self):
        form = self.driver.find_element(By.ID, "filter-form")

        submit_buttons = form.find_elements(
            By.XPATH,
            ".//button[@type='submit'] | .//button[contains(text(), 'Найти')] | .//button[contains(text(), 'Применить')] | .//button[contains(text(), 'Поиск')] | .//input[@type='submit']"
        )

        if submit_buttons:
            button = submit_buttons[0]
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            self.driver.execute_script("arguments[0].click();", button)
        else:
            self.driver.execute_script("arguments[0].submit();", form)


    def click_reset_filters(self):
        self.open()

    def wait_for_filters_applied(self, timeout: int = 10):
        import time
        time.sleep(2)
        
        loaders = self.driver.find_elements(By.CSS_SELECTOR, ".loader, .spinner, .loading, .preloader")
        if loaders:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(
                    (By.CSS_SELECTOR, ".loader, .spinner, .loading, .preloader")
                )
            )

    def assert_program_exists(self, title: str, timeout: int = 10):
        self.assert_visible_text(
            f"//h3[{self.text_predicate(title)}] | //*[contains(@class, 'title')][{self.text_predicate(title)}]",
            timeout
        )

    def assert_program_not_exists(self, title: str, timeout: int = 5):
        elements = self.driver.find_elements(
            By.XPATH,
            f"//h3[{self.text_predicate(title)}] | //*[contains(@class, 'title')][{self.text_predicate(title)}]"
        )
        if elements:
            raise AssertionError(f"Программа '{title}' найдена, хотя не должна была быть отображена")

    def assert_all_programs_match_filter(self, expected_text: str):
        programs = self.driver.find_elements(
            By.CSS_SELECTOR, ".edu-program__item, .education-program-card"
        )

        for program in programs:
            text_content = program.text.lower()
            if expected_text.lower() not in text_content:
                raise AssertionError(
                    f"Программа не соответствует фильтру. Ожидался текст: '{expected_text}'"
                )
