from pages.index import IndexPage
from pages.kontakty.KontaktyIndexPage import KontaktyIndexPage


def test_media(driver):
    index_page = IndexPage(driver)
    index_page.open()
    index_page.assert_h1()
    index_page.open_contacts()

    kontakty_index_page = KontaktyIndexPage(driver)
    kontakty_index_page.assert_h1()


def test_why_susu_slider(driver):
    index_page = IndexPage(driver)
    index_page.open()
    index_page.click_why_susu()
    index_page.assert_postupai_uvereno()
    index_page.assert_vysshikh()
    index_page.click_next_about_slide()
    index_page.assert_22000()
    index_page.click_prev_about_slide()
    index_page.assert_vysshikh()


def test_career_section(driver):
    index_page = IndexPage(driver)
    index_page.open()
    index_page.click_why_susu()
    index_page.click_to_career()
    index_page.assert_sotrudnichestvo()
    index_page.assert_career_center()

def test_prioritet_section(driver):
    index_page = IndexPage(driver)
    index_page.open()
    index_page.click_why_susu()
    index_page.click_to_career()
    index_page.click_to_prioritet()
    index_page.assert_prioritet()


def test_development_section(driver):
    index_page = IndexPage(driver)
    index_page.open()
    index_page.scroll_to_development()
    index_page.assert_development_slide("Центр ИТ-компетенций")
    index_page.click_next_development_slide()
    index_page.assert_development_slide("Центр технологического лидерства")
    index_page.click_next_development_slide()
    index_page.assert_development_slide("Естественные науки")
    index_page.click_next_development_slide()
    index_page.assert_development_slide("Современное социально-гуманитарное")
    index_page.click_prev_development_slide()
    index_page.assert_development_slide("Естественные науки")


def test_military_section(driver):
    index_page = IndexPage(driver)
    index_page.open()
    index_page.click_why_susu()
    index_page.scroll_to_military()
    index_page.assert_military_center()


def test_live_section(driver):
    index_page = IndexPage(driver)
    index_page.open()
    index_page.click_why_susu()
    index_page.scroll_to_live_center()
    index_page.assert_live_center()
    index_page.assert_live_slide("Центр творчества ЮУрГУ")
    index_page.click_next_live_slide()
    index_page.assert_live_slide("Cовременная cпортивная инфраструктура")
    index_page.click_next_live_slide()
    index_page.assert_live_slide("Молодежные общественные организации")
    index_page.click_prev_live_slide()
    index_page.assert_live_slide("Cовременная cпортивная инфраструктура")


def test_admission_section(driver):
    index_page = IndexPage(driver)
    index_page.open()
    index_page.scroll_to_admission()
    index_page.assert_admission_title()


def test_education_programs_section(driver):
    index_page = IndexPage(driver)
    index_page.open()
    index_page.scroll_to_education_programs()
    index_page.assert_education_programs_title()
    index_page.assert_all_programs_link()


def test_steps_section(driver):
    index_page = IndexPage(driver)
    index_page.open()
    index_page.scroll_to_steps()
    index_page.assert_steps_title()
    index_page.assert_step("Выбор направлений подготовки")
    index_page.assert_step("Подача документов")
    index_page.assert_step("Вступительные испытания")
    index_page.assert_step("Зачисление")
