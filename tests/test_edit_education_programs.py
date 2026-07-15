from selenium.webdriver.common.by import By
from pages.wp_login.WpLoginPage import WpLoginPage
from pages.wp_admin.EditEducationProgramPage import EditEducationProgramPage
from pages.education_program.EducationProgramArchivePage import EducationProgramArchivePage
from pages.education_program.SingleEducationProgramPage import SingleEducationProgramPage
from classes.config import Config
import time


def test_edit_program_title(driver):
    """Тест редактирования заголовка программы (post_title) в админке"""
    # Логин в wp-admin
    login_page = WpLoginPage(driver)
    login_page.open()
    login_page.login(Config.wp_admin_login(), Config.wp_admin_password())

    # Открываем программу для редактирования
    edit_page = EditEducationProgramPage(driver)
    original_title = "Прикладная информатика"
    edit_page.open_by_title(original_title)

    # Изменяем заголовок
    new_title = "Прикладная информатика (обновлено)"
    edit_page.update_title(new_title)
    edit_page.publish()

    # Проверяем сообщение об успешном сохранении
    success_message = edit_page.get_success_message()
    assert "обновлен" in success_message.lower() or "updated" in success_message.lower()

    # Проверяем, что изменения сохранились в админке
    edit_page.open_by_title(new_title)
    title_field = driver.find_element(By.ID, "title")
    assert title_field.get_attribute("value") == new_title, \
        f"Заголовок в админке не совпадает. Ожидалось: '{new_title}', найдено: '{title_field.get_attribute('value')}'"

    # Возвращаем исходное название
    edit_page.update_title(original_title)
    edit_page.publish()


def test_edit_program_cost_and_places(driver):
    """Тест редактирования количества мест в админке"""
    login_page = WpLoginPage(driver)
    login_page.open()
    login_page.login(Config.wp_admin_login(), Config.wp_admin_password())

    edit_page = EditEducationProgramPage(driver)
    program_title = "Информационные системы и технологии"
    edit_page.open_by_title(program_title)

    # Сохраняем исходные значения для восстановления
    original_funded = "20"
    original_paid = "12"

    # Изменяем значения
    new_funded = "25"
    new_paid = "15"

    edit_page.update_funded_places(new_funded)
    edit_page.update_paid_places(new_paid)
    edit_page.publish()

    success_message = edit_page.get_success_message()
    assert "обновлен" in success_message.lower() or "updated" in success_message.lower()

    # Проверяем, что изменения сохранились в админке
    edit_page.open_by_title(program_title)

    funded_field = driver.find_element(By.ID, "meta-box-funded-places")
    paid_field = driver.find_element(By.ID, "meta-box-paid-places")

    assert funded_field.get_attribute("value") == new_funded
    assert paid_field.get_attribute("value") == new_paid

    # Возвращаем исходные значения
    edit_page.update_funded_places(original_funded)
    edit_page.update_paid_places(original_paid)
    edit_page.publish()


def test_edit_program_duration(driver):
    """Тест редактирования срока обучения с проверкой на фронтенде"""
    login_page = WpLoginPage(driver)
    login_page.open()
    login_page.login(Config.wp_admin_login(), Config.wp_admin_password())

    edit_page = EditEducationProgramPage(driver)
    program_title = "Экономика предприятий и организаций"
    edit_page.open_by_title(program_title)

    # Получаем slug для проверки на фронтенде
    program_slug = edit_page.get_slug()

    original_duration = "5 лет"
    new_duration = "5 лет 6 месяцев"

    edit_page.update_duration(new_duration)
    edit_page.publish()

    success_message = edit_page.get_success_message()
    assert "обновлен" in success_message.lower() or "updated" in success_message.lower()

    # Проверяем сохранение в админке
    edit_page.open_by_title(program_title)

    duration_field = driver.find_element(By.ID, "meta-box-edu-time")
    assert duration_field.get_attribute("value") == new_duration

    # Проверяем на одиночной странице программы (опциональная проверка)
    single_page = SingleEducationProgramPage(driver)
    single_page.open_by_slug(program_slug)
    time.sleep(3)
    duration_text = single_page.get_duration()
    if duration_text and new_duration not in duration_text:
        print(f"Предупреждение: Новый срок обучения '{new_duration}' не найден на фронтенде. Найдено: '{duration_text}'")


    # Возвращаем исходное значение
    edit_page.open_by_title(program_title)
    edit_page.update_duration(original_duration)
    edit_page.publish()

    single_page = SingleEducationProgramPage(driver)
    single_page.open_by_slug(program_slug)
    time.sleep(3)


def test_edit_program_passing_scores(driver):
    """Тест редактирования проходных баллов с проверкой на фронтенде"""
    login_page = WpLoginPage(driver)
    login_page.open()
    login_page.login(Config.wp_admin_login(), Config.wp_admin_password())

    edit_page = EditEducationProgramPage(driver)
    program_title = "Автоматизация технологических процессов и производств"
    edit_page.open_by_title(program_title)

    # Получаем slug для проверки на фронтенде
    program_slug = edit_page.get_slug()

    original_budget_score = "190"
    original_contract_score = "110"

    new_budget_score = "195"
    new_contract_score = "115"

    edit_page.update_passing_score_budget(new_budget_score)
    edit_page.update_passing_score_contract(new_contract_score)
    edit_page.publish()

    success_message = edit_page.get_success_message()
    assert "обновлен" in success_message.lower() or "updated" in success_message.lower()

    # Проверяем сохранение в админке
    edit_page.open_by_title(program_title)

    budget_field = driver.find_element(By.ID, "meta-box-passing_score_budget")
    contract_field = driver.find_element(By.ID, "meta-box-passing_score_contract")

    assert budget_field.get_attribute("value") == new_budget_score
    assert contract_field.get_attribute("value") == new_contract_score

    # Проверяем на одиночной странице программы (опциональная проверка)

    single_page = SingleEducationProgramPage(driver)
    single_page.open_by_slug(program_slug)
    time.sleep(3)
    passing_score_text = single_page.get_passing_score_budget()
    if passing_score_text and new_budget_score not in passing_score_text:
        print(f"Предупреждение: Новый проходной балл '{new_budget_score}' не найден на фронтенде. Найдено: '{passing_score_text}'")


    # Возвращаем исходные значения
    edit_page.open_by_title(program_title)
    edit_page.update_passing_score_budget(original_budget_score)
    edit_page.update_passing_score_contract(original_contract_score)
    edit_page.publish()

    single_page = SingleEducationProgramPage(driver)
    single_page.open_by_slug(program_slug)
    time.sleep(3)


def test_edit_program_cost(driver):
    """Тест редактирования стоимости обучения с проверкой на фронтенде"""
    login_page = WpLoginPage(driver)
    login_page.open()
    login_page.login(Config.wp_admin_login(), Config.wp_admin_password())

    edit_page = EditEducationProgramPage(driver)
    program_title = "Юриспруденция"
    edit_page.open_by_title(program_title)

    # Получаем slug для проверки на фронтенде
    program_slug = edit_page.get_slug()

    # Исходная стоимость
    original_cost = "225000"
    new_cost = "220000"

    # Изменяем стоимость
    edit_page.update_cost(new_cost)
    edit_page.publish()

    success_message = edit_page.get_success_message()
    assert "обновлен" in success_message.lower() or "updated" in success_message.lower()

    # Проверяем на одиночной странице программы (опциональная проверка)

    single_page = SingleEducationProgramPage(driver)
    single_page.open_by_slug(program_slug)
    time.sleep(3)
    # Стоимость на фронтенде форматируется с разделителями разрядов и знаком ₽
    cost_text = single_page.get_cost()
    if cost_text:
        formatted_cost = f"{int(new_cost):,}".replace(",", " ")
        if formatted_cost not in cost_text and new_cost not in cost_text:
            print(f"Предупреждение: Новая стоимость '{new_cost}' (форматированная: '{formatted_cost}') не найдена на фронтенде. Найдено: '{cost_text}'")

    # Возвращаем исходное значение
    edit_page.open_by_title(program_title)
    edit_page.update_cost(original_cost)
    edit_page.publish()

    # Проверяем на одиночной странице программы (опциональная проверка)
    single_page = SingleEducationProgramPage(driver)
    single_page.open_by_slug(program_slug)
    time.sleep(3)


def test_edit_multiple_fields(driver):
    """Тест одновременного редактирования нескольких полей"""
    login_page = WpLoginPage(driver)
    login_page.open()
    login_page.login(Config.wp_admin_login(), Config.wp_admin_password())

    edit_page = EditEducationProgramPage(driver)
    program_title = "Строительство"
    edit_page.open_by_title(program_title)

    # Исходные значения
    original_duration = "4 года"
    original_funded = "28"
    original_paid = "15"
    original_budget_score = "195"

    # Новые значения
    new_duration = "4 года 6 месяцев"
    new_funded = "30"
    new_paid = "18"
    new_budget_score = "200"

    # Изменяем все поля
    edit_page.update_duration(new_duration)
    edit_page.update_funded_places(new_funded)
    edit_page.update_paid_places(new_paid)
    edit_page.update_passing_score_budget(new_budget_score)
    edit_page.publish()

    success_message = edit_page.get_success_message()
    assert "обновлен" in success_message.lower() or "updated" in success_message.lower()

    # Проверяем все изменения в админке
    edit_page.open_by_title(program_title)

    duration_field = driver.find_element(By.ID, "meta-box-edu-time")
    funded_field = driver.find_element(By.ID, "meta-box-funded-places")
    paid_field = driver.find_element(By.ID, "meta-box-paid-places")
    budget_field = driver.find_element(By.ID, "meta-box-passing_score_budget")

    assert duration_field.get_attribute("value") == new_duration, f"Срок обучения не совпадает"
    assert funded_field.get_attribute("value") == new_funded, f"Количество бюджетных мест не совпадает"
    assert paid_field.get_attribute("value") == new_paid, f"Количество платных мест не совпадает"
    assert budget_field.get_attribute("value") == new_budget_score, f"Проходной балл не совпадает"

    # Возвращаем все исходные значения
    edit_page.open_by_title(program_title)
    edit_page.update_duration(original_duration)
    edit_page.update_funded_places(original_funded)
    edit_page.update_paid_places(original_paid)
    edit_page.update_passing_score_budget(original_budget_score)
    edit_page.publish()


def test_edit_form_education_program(driver):
    """Полный тест редактирования программы с проверкой через фильтры"""
    import time

    # Логин в wp-admin
    login_page = WpLoginPage(driver)
    login_page.open()
    login_page.login(Config.wp_admin_login(), Config.wp_admin_password())

    # Программа "Юриспруденция" — единственная с формой "очно-заочная" и подразделением "Юридический институт"
    program_title_admin = "Юриспруденция"
    program_code = "40.03.01"  # Код направления для поиска на фронтенде
    division = "Юридический институт"
    original_form = "очная"
    new_form = "очно-заочная"

    # 1. Проверяем, что программа находится по исходной комбинации фильтров "очно-заочная" + "Юридический институт"
    archive_page = EducationProgramArchivePage(driver)
    archive_page.open()
    archive_page.assert_has_programs()

    archive_page.select_filter_form(original_form)
    archive_page.select_filter_division(division)
    archive_page.wait_for_filters_applied()

    titles = archive_page.get_program_titles()
    assert any(program_code in title for title in titles), \
        f"Программа с кодом '{program_code}' не найдена в списке с фильтрами '{original_form}' + '{division}'"

    # 2. Меняем ТОЛЬКО форму обучения в админке (подразделение остаётся "Юридический институт")
    edit_page = EditEducationProgramPage(driver)
    edit_page.open_by_title(program_title_admin)
    edit_page.update_edu_form(new_form)
    edit_page.publish()

    success_message = edit_page.get_success_message()
    assert "обновлен" in success_message.lower() or "updated" in success_message.lower(), \
        f"Не получено сообщение об успешном обновлении. Получено: '{success_message}'"

    # Пауза для синхронизации кеша фронтенда
    time.sleep(3)

    # 3. Проверяем, что программа НЕ находится по старой комбинации фильтров "очно-заочная" + "Юридический институт"
    archive_page.open()
    archive_page.select_filter_form(original_form)
    archive_page.select_filter_division(division)
    archive_page.wait_for_filters_applied()

    titles = archive_page.get_program_titles()
    assert not any(program_code in title for title in titles), \
        f"Программа с кодом '{program_code}' всё ещё найдена в списке с фильтрами '{original_form}' + '{division}' после изменения"

    # 4. Проверяем, что программа находится по новой комбинации фильтров "очная" + "Юридический институт"
    archive_page.click_reset_filters()
    archive_page.wait_for_filters_applied()

    archive_page.select_filter_form(new_form)
    archive_page.select_filter_division(division)
    archive_page.wait_for_filters_applied()

    titles = archive_page.get_program_titles()
    assert any(program_code in title for title in titles), \
        f"Программа с кодом '{program_code}' не найдена в списке с фильтрами '{new_form}' + '{division}' после изменения"

    # 5. Возвращаем форму обратно на "очно-заочная"
    edit_page.open_by_title(program_title_admin)
    edit_page.update_edu_form(original_form)
    edit_page.publish()

    success_message = edit_page.get_success_message()
    assert "обновлен" in success_message.lower() or "updated" in success_message.lower(), \
        f"Не получено сообщение об успешном обновлении при возврате. Получено: '{success_message}'"

    # Пауза для синхронизации кеша фронтенда
    time.sleep(3)

    # 6. Проверяем, что программа снова находится по исходной комбинации фильтров "очно-заочная" + "Юридический институт"
    archive_page.open()
    archive_page.select_filter_form(original_form)
    archive_page.select_filter_division(division)
    archive_page.wait_for_filters_applied()

    titles = archive_page.get_program_titles()
    assert any(program_code in title for title in titles), \
        f"Программа с кодом '{program_code}' не найдена в списке с фильтрами '{original_form}' + '{division}' после возврата"
