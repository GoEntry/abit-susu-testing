import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pages.base.admin.page import AdminPage
from components.fields.tinymce import TinymceField
class TermPage(AdminPage):
    taxonomy: str
    def open(self):
        super().open(f"/wp-admin/edit-tags.php?taxonomy={self.taxonomy}&post_type=education-program")

    def add_term(
        self,
        name: str,
        image_path: str = None,
        pdf_path: str = None,
        description: str = None,
        content: str = None,
        timeout: int = 10,
    ):
        self.driver.find_element(By.ID, "tag-name").send_keys(name)
        if description:
            self.driver.find_element(By.ID, "tag-description").send_keys(description)
        if content:
            # Доп. rich-text поле у некоторых таксономий (Контакты — "Контакты
            # описание", Профессии — "Профессия после обучения"): по умолчанию
            # уже в режиме "Код" (обычная <textarea class="wp-editor-area">),
            # поэтому send_keys работает напрямую, без обращения к TinyMCE API.
            # Ищем в контексте формы добавления термина, чтобы не переключаться
            # между несколькими редакторами на странице.
            TinymceField(self.driver, f"{self.taxonomy}-content_ifr", content).handle()
            # form = self.driver.find_element(By.ID, "addtag")
            # form_descrition = WebDriverWait(form, 3).until(
            #     EC.presence_of_element_located((By.CSS_SELECTOR,".wp-editor-area"))
            # )
            # form_descrition.send_keys(content)
        if image_path:
            self._upload_image(image_path, timeout)
        if pdf_path:
            self._upload_pdf(pdf_path, timeout)
        self.driver.find_element(By.ID, "submit").click()
        self.assert_visible_text(f"//tr[{self.text_predicate(name)}]", timeout)

    def _upload_image(self, path: str, timeout: int):
        # Только у некоторых таксономий (Партнёры/Профессии/Контакты) в форме
        # добавления термина есть поле картинки — стандартный медиа-загрузчик
        # WordPress (.upload_image_button открывает .media-modal). Кнопку
        # "Выберите файлы" не кликаем — она открывает системный диалог выбора
        # файла, с которым Selenium работать не может; вместо этого файл
        # передаётся напрямую в скрытый <input type="file">, который уже есть
        # в DOM модалки сразу после её открытия.
        self.driver.find_element(By.CSS_SELECTOR, ".upload_image_button").click()

        # Каждый клик по кнопке создаёт НОВЫЙ экземпляр .media-modal, а
        # предыдущие остаются в DOM (не удаляются) — при добавлении
        # нескольких терминов подряд на одной странице глобальный поиск
        # `.media-modal` находил бы первый, уже закрытый модал. Берём
        # последний по порядку в DOM — это всегда самый свежий.
        modal = WebDriverWait(self.driver, timeout).until(
            lambda driver: driver.find_elements(By.CSS_SELECTOR, ".media-modal")[-1]
        )
        file_input = WebDriverWait(self.driver, timeout).until(
            lambda driver: modal.find_element(By.CSS_SELECTOR, "input[type='file']")
        )
        file_input.send_keys(os.path.abspath(path))

        select_button = WebDriverWait(self.driver, timeout).until(
            lambda driver: modal.find_element(By.CSS_SELECTOR, ".media-button-select")
        )
        WebDriverWait(self.driver, timeout).until(lambda driver: select_button.is_enabled())
        select_button.click()

        # Ждём не закрытия модалки (её DOM-узел остаётся, просто прячется), а
        # того, что #image_id на самой форме термина реально заполнился —
        # это и есть подтверждение, что картинка выбрана.
        WebDriverWait(self.driver, timeout).until(
            lambda driver: driver.find_element(By.ID, "image_id").get_attribute("value")
        )

    def _upload_pdf(self, path: str, timeout: int):
        # У таксономии subjects_spo есть поле загрузки PDF через стандартный
        # медиа-загрузчик WordPress. Кнопка называется "Загрузить файл".
        button_selectors = [
            ".upload_pdf_button",
            ".upload_file_button",
        ]

        button = None
        for selector in button_selectors:
            buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
            if buttons:
                button = buttons[0]
                break

        # Если не нашли по классу, ищем по тексту кнопки
        if not button:
            buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Загрузить файл')] | //input[@type='button' and contains(@value, 'Загрузить файл')]")
            if buttons:
                button = buttons[0]

        if not button:
            # Если кнопка не найдена, пропускаем загрузку
            return

        button.click()

        modal = WebDriverWait(self.driver, timeout).until(
            lambda driver: driver.find_elements(By.CSS_SELECTOR, ".media-modal")[-1]
        )
        file_input = WebDriverWait(self.driver, timeout).until(
            lambda driver: modal.find_element(By.CSS_SELECTOR, "input[type='file']")
        )
        file_input.send_keys(os.path.abspath(path))

        select_button = WebDriverWait(self.driver, timeout).until(
            lambda driver: modal.find_element(By.CSS_SELECTOR, ".media-button-select")
        )
        WebDriverWait(self.driver, timeout).until(lambda driver: select_button.is_enabled())
        select_button.click()

        # Ждём заполнения #pdf_id на форме термина (если такое поле есть)
        WebDriverWait(self.driver, timeout).until(
            lambda driver: driver.find_element(By.ID, "file_id").get_attribute("value")
        )
