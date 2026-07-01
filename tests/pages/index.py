from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base.user.page import UserPage
import time


class IndexPage(UserPage):
    def open(self):
        super().open("")

    def assert_h1(self):
        super().assert_h1("Поступай и учись в ЮУрГУ!")

    def open_contacts(self):
        link = self.driver.find_element(By.LINK_TEXT, "КОНТАКТЫ")
        link.click()

    def _click_swiper_btn(self, selector, pause=0):
        btn = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
        self.driver.execute_script("arguments[0].click();", btn)
        if pause:
            time.sleep(pause)

    def _scroll_to(self, css_selector):
        section = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", section)
        time.sleep(1)

    def _assert_section_heading(self, section_class, text, heading_class="triangle-text", timeout=5):
        self.assert_visible_text(
            f"//*[contains(@class,'{section_class}')]"
            f"//*[contains(@class,'{heading_class}') and {self.text_predicate(text)}]",
            timeout=timeout,
        )

    def _assert_active_slide(self, swiper_class, title_class, text, timeout=5):
        self.assert_visible_text(
            f"//*[contains(@class,'{swiper_class}')]"
            "//*[contains(@class,'swiper-slide-active')]"
            f"//*[contains(@class,'{title_class}') and {self.text_predicate(text)}]",
            timeout=timeout,
        )

    def click_why_susu(self):
        btn = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".more-content")))
        btn.click()
        time.sleep(3)

    def assert_postupai_uvereno(self):
        self._assert_section_heading("information-section", "Поступай уверенно!")

    def assert_vysshikh(self):
        self._assert_active_slide("swiper-home-about", "number-block__schools_text", "высших")

    def click_next_about_slide(self):
        self._click_swiper_btn(".home-about-button__next", pause=1)

    def click_prev_about_slide(self):
        self._click_swiper_btn(".home-about-button__prev", pause=1)

    def assert_22000(self):
        self._assert_active_slide("swiper-home-about", "number-block__students_number", "22000")

    def click_to_career(self):
        arrow = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#career']"))
        )
        arrow.click()
        time.sleep(3)

    def assert_sotrudnichestvo(self):
        self.assert_visible_text(f"//h3[contains(@class,'cooperation-text') and {self.text_predicate('Сотрудничество')}]")

    def assert_career_center(self):
        self.assert_visible_text(
            f"//*[contains(@class,'cooperation__content')]//h2[{self.text_predicate('Центр карьеры')}]",
            timeout=10,
        )

    def click_to_prioritet(self):
        arrow = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#career .scroll-arrow"))
        )
        self.driver.execute_script("arguments[0].click();", arrow)
        time.sleep(3)

    def assert_prioritet(self):
        self.assert_visible_text(f"//*[contains(@class,'innovation-block__number_text') and {self.text_predicate('Приоритет')}]")

    def scroll_to_development(self):
        self._scroll_to(".development-section")

    def assert_development_slide(self, text):
        self._assert_active_slide("swiper-home-development", "development-slider__title", text, timeout=10)

    def click_next_development_slide(self):
        self._click_swiper_btn(".home-development-button__next", pause=1)

    def click_prev_development_slide(self):
        self._click_swiper_btn(".home-development-button__prev", pause=1)

    def scroll_to_military(self):
        self._scroll_to(".military-section")
        time.sleep(1)

    def assert_military_center(self):
        self._assert_section_heading("military-section", "Военный учебный центр", timeout=10)

    def scroll_to_live_center(self):
        self._scroll_to(".live-section")

    def assert_live_center(self):
        self._assert_section_heading("live-section", "Центр притяжения и развития талантов", timeout=10)

    def assert_live_slide(self, text):
        self._assert_active_slide("live-section", "live-slider__title", text, timeout=10)

    def click_next_live_slide(self):
        self._click_swiper_btn(".home-live-button__next", pause=1)

    def click_prev_live_slide(self):
        self._click_swiper_btn(".home-live-button__prev", pause=1)

    def scroll_to_admission(self):
        self._scroll_to(".admission")
        time.sleep(1)

    def assert_admission_title(self):
        self._assert_section_heading(
            "admission", "Начни новую жизнь прямо сейчас!", heading_class="title-h2", timeout=10
        )

    def scroll_to_education_programs(self):
        self._scroll_to(".education-section")
        time.sleep(1)

    def assert_education_programs_title(self):
        self._assert_section_heading(
            "education-section", "Программы подготовки", heading_class="title-h2", timeout=10
        )

    def assert_all_programs_link(self):
        self.assert_visible_text(
            f"//*[contains(@class,'edu-programs-all')]//a[{self.text_predicate('Все программы')}]",
            timeout=10,
        )

    def scroll_to_steps(self):
        self._scroll_to(".steps")
        time.sleep(1)

    def assert_steps_title(self):
        self._assert_section_heading("steps", "Как стать студентом", heading_class="title-h2", timeout=10)

    def assert_step(self, text):
        self._assert_section_heading("steps", text, heading_class="step__heading", timeout=10)
