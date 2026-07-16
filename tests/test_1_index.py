from pages.index import IndexPage
from pages.kontakty.KontaktyIndexPage import KontaktyIndexPage


def test_first_part(driver):
    index_page = IndexPage(driver)
    index_page.open()
    index_page.assert_h1()
    index_page.open_contacts()

    kontakty_index_page = KontaktyIndexPage(driver)
    kontakty_index_page.assert_h1()

    index_page.open()
    index_page.click_why_susu()
    index_page.assert_postupai_uvereno()
    index_page.assert_vysshikh()
    index_page.click_next_about_slide()
    index_page.assert_22000()
    index_page.click_prev_about_slide()
    index_page.assert_vysshikh()

    index_page.click_to_career()
    index_page.assert_sotrudnichestvo()
    index_page.assert_career_center()

    index_page.click_to_prioritet()
    index_page.assert_prioritet()

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

    index_page.scroll_to_military()
    index_page.assert_military_center()

    index_page.scroll_to_live_center()
    index_page.assert_live_center()
    index_page.assert_live_slide("Центр творчества ЮУрГУ")
    index_page.click_next_live_slide()
    index_page.assert_live_slide("Современная cпортивная инфраструктура")
    index_page.click_next_live_slide()
    index_page.assert_live_slide("Молодежные общественные организации")
    index_page.click_prev_live_slide()
    index_page.assert_live_slide("Современная cпортивная инфраструктура")

    index_page.scroll_to_admission()
    index_page.assert_admission_title()

    index_page.scroll_to_education_programs()
    index_page.assert_education_programs_title()
    index_page.assert_all_programs_link()

    index_page.scroll_to_steps()
    index_page.assert_steps_title()
    index_page.assert_step("Выбор направлений подготовки")
    index_page.assert_step("Подача документов")
    index_page.assert_step("Вступительные испытания")
    index_page.assert_step("Зачисление")

    index_page.scroll_to_qa()
    index_page.assert_qa_title()
    index_page.assert_qa_question(1, "Куда я могу поступить со своим набором ЕГЭ?")
    index_page.assert_qa_question(6, "Нужно ли сдавать внутренние вступительные испытания (ДВИ)?")
    index_page.assert_qa_question(11, "Как я узнаю, что прошёл по баллам и меня зачислили?")

    index_page.click_qa_question(1)
    index_page.assert_qa_answer_visible(1)
    index_page.click_qa_question(6)
    index_page.assert_qa_answer_visible(6)
    index_page.click_qa_question(11)
    index_page.assert_qa_answer_visible(11)

    index_page.click_qa_question(1)
    index_page.assert_qa_answer_hidden(1)
    index_page.click_qa_question(6)
    index_page.assert_qa_answer_hidden(6)
    index_page.click_qa_question(11)
    index_page.assert_qa_answer_hidden(11)


def test_second_part(driver):
    index_page = IndexPage(driver)
    index_page.open()

    index_page.scroll_to_calendar()
    index_page.assert_calendar_title()
    index_page.assert_calendar_tab_visible("bakalavriat-speczialitet")
    index_page.click_calendar_tab("magistratura")
    index_page.assert_calendar_tab_visible("magistratura")
    index_page.click_calendar_tab("aspirantura")
    index_page.assert_calendar_tab_visible("aspirantura")
    index_page.click_calendar_tab("spo")
    index_page.assert_calendar_tab_visible("spo")

    index_page.scroll_to_infrastructure()
    index_page.assert_video_visible()
    index_page.assert_infrastructure_title()
    index_page.assert_infrastructure_slide("Студенческий городок Южно-Уральского государственного университета")
    index_page.click_next_infrastructure_slide()
    index_page.assert_infrastructure_slide("Межуниверситетский кампус")
    index_page.click_next_infrastructure_slide()
    index_page.assert_infrastructure_slide("Питание")
    index_page.click_prev_infrastructure_slide()
    index_page.assert_infrastructure_slide("Межуниверситетский кампус")

    index_page.scroll_to_admissions_committee()
    index_page.assert_admissions_committee_title()

