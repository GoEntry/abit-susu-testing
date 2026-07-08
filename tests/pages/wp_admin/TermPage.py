import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pages.base.admin.page import AdminPage

class TermPage(AdminPage):
    def open(self, taxonomy: str):
        super().open(f"/wp-admin/edit-tags.php?taxonomy={taxonomy}&post_type=education-program")

    def add_term(
        self,
        name: str,
        image_path: str = None,
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
            self.driver.find_element(By.CSS_SELECTOR, ".wp-editor-area").send_keys(content)
        if image_path:
            self._upload_image(image_path, timeout)
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
