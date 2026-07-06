from selenium.common.exceptions import TimeoutException
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
        Select2Field(self.driver, "extra[edu-area]", program["edu_area"]).handle()
        Select2Field(self.driver, "extra[edu-form]", program["edu_form"]).handle()
        Select2Field(self.driver, "extra[branches]", program["branch"]).handle()
        Select2Field(self.driver, "extra[division]", program["division"]).handle()
        Select2Field(self.driver, "extra[subjects-ege][]", program["exam_subjects"]).handle()
        Select2Field(self.driver, "extra[funded-places-fields][]", program["funded_place_types"]).handle()
        Select2Field(self.driver, "extra[partners][]", program["partners"]).handle()
        Select2Field(self.driver, "extra[profiles][]", program["profiles"]).handle()
        Select2Field(self.driver, "extra[edu-professions][]", program["professions"]).handle()
        Select2Field(self.driver, "extra[contacts-tax][]", program["contacts"]).handle()

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
