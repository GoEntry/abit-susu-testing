from selenium.common.exceptions import ElementNotInteractableException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from components.fields.select2 import Select2Field
from pages.base.admin.page import AdminPage

class AddEducationProgramPage(AdminPage):
    def open(self):
        super().open("/wp-admin/post-new.php?post_type=education-program")

    def fill_program(self, program: dict):
        self.driver.find_element(By.ID, "title").send_keys(program["title"])
        self.fill_select2_fields(program)

        Select(self.driver.find_element(By.NAME, "extra[edu-cost]")).select_by_visible_text(program["edu_cost"])
        Select(self.driver.find_element(By.NAME, "extra[language]")).select_by_value(program["language_value"])
        Select(self.driver.find_element(By.NAME, "extra[view-front-page]")).select_by_value(
            program["front_page_position_value"]
        )

        self.driver.find_element(By.ID, "meta-box-edu-time").send_keys(program["duration"])
        self.driver.find_element(By.ID, "meta-box-funded-places").send_keys(program["funded_places_total"])
        self.driver.find_element(By.ID, "meta-box-paid-places").send_keys(program["paid_places"])
        self.driver.find_element(By.ID, "meta-box-passing_score_budget").send_keys(program["passing_score_budget"])
        self.driver.find_element(By.ID, "meta-box-passing_score_contract").send_keys(program["passing_score_contract"])

        self._fill_consultations(program["consultations"])

    def fill_select2_fields(self, program: dict):
        self.fill_edu_area(program["edu_area"])
        self.fill_edu_form(program["edu_form"])
        self.fill_branch(program["branch"])
        self.fill_division(program["division"])
        self.fill_exam_subjects(program["exam_subjects"])
        self.fill_funded_place_types(program["funded_place_types"])
        self.fill_partners(program["partners"])
        self.fill_profiles(program["profiles"])
        self.fill_professions(program["professions"])
        self.fill_contacts(program["contacts"])

    def fill_edu_area(self, text: str):
        Select2Field(self.driver, "extra[edu-area]", text).handle()

    def fill_edu_form(self, text: str):
        Select2Field(self.driver, "extra[edu-form]", text).handle()

    def fill_branch(self, text: str):
        Select2Field(self.driver, "extra[branches]", text).handle()

    def fill_division(self, text: str):
        Select2Field(self.driver, "extra[division]", text).handle()

    def fill_exam_subjects(self, texts: list):
        Select2Field(self.driver, "extra[subjects-ege][]", texts).handle()

    def fill_funded_place_types(self, texts: list):
        Select2Field(self.driver, "extra[funded-places-fields][]", texts).handle()

    def fill_partners(self, texts: list):
        Select2Field(self.driver, "extra[partners][]", texts).handle()

    def fill_profiles(self, texts: list):
        Select2Field(self.driver, "extra[profiles][]", texts).handle()

    def fill_professions(self, texts: list):
        Select2Field(self.driver, "extra[edu-professions][]", texts).handle()

    def fill_contacts(self, texts: list):
        Select2Field(self.driver, "extra[contacts-tax][]", texts).handle()

    def fill_exam_details(self, exam_details: dict):
        for subject, (exam_type, order) in exam_details.items():
            row = self.driver.find_element(By.XPATH, f"//tr[td/label[{self.text_predicate(subject)}]]")
            Select(row.find_element(By.TAG_NAME, "select")).select_by_value(exam_type)
            row.find_element(By.CSS_SELECTOR, "input[type='text']").send_keys(order)

    def fill_funded_place_counts(self, counts: dict):
        for label, count in counts.items():
            xpath = (
                "//div[contains(@class, 'funded-place-fields-input')]"
                f"//label[{self.text_predicate(label)}]/following-sibling::input[1]"
            )
            self.driver.find_element(By.XPATH, xpath).send_keys(count)

    def fill_profile_details(self, profile_details: dict):
        # profile_details: {"Название профиля": ("текст образовательной программы", "текст компетенций")}.
        # Как и с испытаниями/бюджетными местами — блок на каждый выбранный
        # профиль появляется только после первой публикации. Внешне выглядит
        # как аккордеон (<details>/<summary>), но тема принудительно держит
        # его развёрнутым через CSS (display: block), поэтому кликать по
        # summary не нужно — оба textarea сразу доступны и уже в режиме "Код".
        for profile_name, (edu_program_text, competencies_text) in profile_details.items():
            print(f"//details[contains(@class, 'profile-accordion')][summary[{self.text_predicate(profile_name)}]]")
            block = self.driver.find_element(
                By.XPATH,
                f"//details[contains(@class, 'profile-accordion')][summary[{self.text_predicate(profile_name)}]]",
            )
            edu_program_field, competencies_field = block.find_elements(By.TAG_NAME, "textarea")
            self._fill_textarea(edu_program_field, edu_program_text)
            self._fill_textarea(competencies_field, competencies_text)

    def _fill_textarea(self, field, text: str):
        # Тот же баг сайта, что и с "Консультациями" (сторонний скрипт
        # CodeMirror иногда ломает инициализацию редакторов на странице) —
        # изредка эта textarea на мгновение недоступна для send_keys сразу
        # после навигации. В этом случае подставляем значение прямо в DOM.
        try:
            field.send_keys(text)
        except ElementNotInteractableException:
            self.driver.execute_script("arguments[0].value = arguments[1];", field, text)

    def publish(self, timeout: int = 15):
        button = self.driver.find_element(By.ID, "publish")
        button.click()
        WebDriverWait(self.driver, timeout).until(EC.staleness_of(button))

    def _fill_consultations(self, html: str, timeout: int = 10):
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script(
                    "return typeof tinymce !== 'undefined' && tinymce.get('field-consultations') !== null;"
                )
            )
            self.driver.execute_script(
                "tinymce.get('field-consultations').setContent(arguments[0]);", html
            )
        except TimeoutException:
            self.driver.execute_script(
                "document.getElementById('field-consultations').value = arguments[0];", html
            )
