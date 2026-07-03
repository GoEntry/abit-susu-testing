from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base.admin.page import AdminPage

class AddEducationProgramPage(AdminPage):
    def open(self):
        super().open("/wp-admin/post-new.php?post_type=education-program")

    def fill_program(self, program: dict):
        self.driver.find_element(By.ID, "title").send_keys(program["title"])

        self._set_select_by_text("extra[edu-area]", program["edu_area"])
        self._set_select_by_text("extra[edu-cost]", program["edu_cost"])
        self._set_multiselect_by_texts("extra[subjects-ege][]", program["exam_subjects"])
        self._set_multiselect_by_texts("extra[funded-places-fields][]", program["funded_place_types"])
        self._set_multiselect_by_texts("extra[partners][]", program["partners"])
        self._set_multiselect_by_texts("extra[profiles][]", program["profiles"])
        self._set_multiselect_by_texts("extra[edu-professions][]", program["professions"])
        self._set_multiselect_by_texts("extra[contacts-tax][]", program["contacts"])

        self._set_select("extra[edu-form]", program["edu_form_value"])
        self._set_select("extra[branches]", program["branch_value"])
        self._set_select("extra[division]", program["division_value"])
        self._set_select("extra[language]", program["language_value"])
        self._set_select("extra[view-front-page]", program["front_page_position_value"])

        self.driver.find_element(By.ID, "meta-box-edu-time").send_keys(program["duration"])
        self.driver.find_element(By.ID, "meta-box-funded-places").send_keys(program["funded_places_total"])
        self.driver.find_element(By.ID, "meta-box-paid-places").send_keys(program["paid_places"])
        self.driver.find_element(By.ID, "meta-box-passing_score_budget").send_keys(program["passing_score_budget"])
        self.driver.find_element(By.ID, "meta-box-passing_score_contract").send_keys(program["passing_score_contract"])
        self.driver.find_element(By.ID, "meta-box-profile").send_keys(program["profiles"][0])

        self.driver.execute_script(
            "tinymce.get('field-consultations').setContent(arguments[0]);", program["consultations"]
        )

    def fill_exam_details(self, exam_details: dict):
        # exam_details: {"Название предмета": ("1" - обязательный/"0" - по выбору, "порядок вывода")}.
        # Строки таблицы появляются только после первой публикации (рендерятся
        # сервером по уже сохранённым extra[subjects-ege][]), поэтому это
        # отдельный шаг, а не часть fill_program().
        script = """
            const [subject, examType, order] = arguments;
            const row = [...document.querySelectorAll('.subjects-ege-fields table tr')]
                .find(r => r.querySelector('td label')?.textContent.trim() === subject);
            const select = row.querySelector('select');
            const input = row.querySelector('input[type="text"]');
            select.value = examType;
            input.value = order;
            jQuery(select).trigger('change');
        """
        for subject, (exam_type, order) in exam_details.items():
            self.driver.execute_script(script, subject, exam_type, order)

    def fill_funded_place_counts(self, counts: dict):
        # counts: {"Название типа мест": "количество"}. Как и с испытаниями,
        # поля появляются только после первой публикации.
        script = """
            const [label, count] = arguments;
            const container = document.querySelector('.funded-place-fields-input');
            const labelEl = [...container.querySelectorAll('label')].find(l => l.textContent.trim() === label);
            labelEl.nextElementSibling.value = count;
        """
        for label, count in counts.items():
            self.driver.execute_script(script, label, count)

    def publish(self, timeout: int = 15):
        # Публикация/обновление перезагружает страницу (создание — с редиректом
        # на экран редактирования, обновление — той же страницей), поэтому
        # ждём протухания старой кнопки как признака завершённой навигации —
        # иначе следующий шаг (например, fill_exam_details) может выполниться
        # ещё до того, как отрендерятся серверные репитеры на новой странице.
        button = self.driver.find_element(By.ID, "publish")
        button.click()
        WebDriverWait(self.driver, timeout).until(EC.staleness_of(button))

    def _set_select(self, name: str, value):
        script = """
            const select = document.querySelector(`select[name="${arguments[0]}"]`);
            select.value = arguments[1];
            jQuery(select).trigger('change');
        """
        self.driver.execute_script(script, name, value)

    def _set_select_by_text(self, name: str, text: str):
        # У терминов таксономий (Направление, Стоимость и т.п.) value — это id
        # термина, который не детерминирован между пересозданиями после
        # сброса БД, поэтому выбираем по видимому тексту.
        script = """
            const select = document.querySelector(`select[name="${arguments[0]}"]`);
            const option = [...select.options].find(o => o.text === arguments[1]);
            select.value = option.value;
            jQuery(select).trigger('change');
        """
        self.driver.execute_script(script, name, text)

    def _set_multiselect_by_texts(self, name: str, texts: list):
        # Поля направления/партнёров/профилей и т.п. используют select2 поверх
        # обычного <select>: реальный клик по виджету открывает динамически
        # генерируемый выпадающий список вне DOM select2, поэтому значения
        # выставляются напрямую через jQuery, как и клики по свайперам в IndexPage.
        script = """
            const select = document.querySelector(`select[name="${arguments[0]}"]`);
            const texts = arguments[1];
            [...select.options].forEach(o => o.selected = texts.includes(o.text));
            jQuery(select).trigger('change');
        """
        self.driver.execute_script(script, name, texts)
