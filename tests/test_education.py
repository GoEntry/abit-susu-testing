from classes.config import Config
from pages.wp_login.WpLoginPage import WpLoginPage
from pages.test.ResetDbPage import ResetDbPage
from pages.wp_admin.EducationProgramListPage import EducationProgramListPage
from pages.wp_admin.AddEducationProgramPage import AddEducationProgramPage
from pages.wp_admin.TermPage import TermPage

EDU_AREA_NAME = "09.03.01 Информатика и вычислительная техника"

# Термины стоимости обучения должны быть просто числом (без пробелов и "₽") —
# фронтенд сам форматирует их с разделителями разрядов и знаком валюты;
# текст вида "220 000 ₽/год" тема обрезает по первому пробелу.
TAXONOMY_TERMS = {
    "edu-areas": [
        "09.03.01 Информатика и вычислительная техника",
        "09.03.02 Информационные системы и технологии",
        "38.03.01 Экономика",
        "15.03.04 Автоматизация технологических процессов и производств",
        "08.03.01 Строительство",
        "40.03.01 Юриспруденция",
    ],
    "subjects": [
        "Русский язык",
        "Математика (профильная)",
        "Информатика и ИКТ",
        "Физика",
        "Обществознание",
        "Иностранный язык",
    ],
    "partners": [
        "ПАО «Ростелеком»",
        "АО «Челябинский трубопрокатный завод»",
        "ООО «Цифровые технологии»",
        "Правительство Челябинской области",
    ],
    "profile": [
        "Разработка программного обеспечения",
        "Информационные системы предприятия",
        "Экономика предприятий и организаций",
        "Автоматизация производственных процессов",
        "Промышленное и гражданское строительство",
        "Гражданское право",
    ],
    "professions": [
        "Программист",
        "Аналитик данных",
        "Экономист",
        "Инженер-технолог",
        "Инженер-строитель",
        "Юрист",
    ],
    "contacts": [
        "Приёмная комиссия ЮУрГУ",
    ],
    "edu-costs": [
        "195000",
        "205000",
        "210000",
        "215000",
        "220000",
        "225000",
    ],
}

PROGRAMS = [
    {
        "title": "Прикладная информатика",
        "edu_area": "09.03.01 Информатика и вычислительная техника",
        "edu_cost": "220000",
        "exam_subjects": ["Русский язык", "Математика (профильная)", "Информатика и ИКТ"],
        "exam_details": {
            "Русский язык": ("1", "1"),
            "Математика (профильная)": ("1", "2"),
            "Информатика и ИКТ": ("0", "3"),
        },
        "funded_place_types": ["Основные места в рамках КЦП", "Целевая квота"],
        "funded_place_counts": {"Основные места в рамках КЦП": "20", "Целевая квота": "5"},
        "partners": ["ООО «Цифровые технологии»"],
        "profiles": ["Разработка программного обеспечения"],
        "professions": ["Программист", "Аналитик данных"],
        "contacts": ["Приёмная комиссия ЮУрГУ"],
        "edu_form_value": "0",  # очная
        "branch_value": "0",  # Челябинск
        "division_value": "3",  # Высшая школа электроники и компьютерных наук
        "language_value": "0",  # Русский
        "front_page_position_value": "0",  # 1
        "duration": "4 года",
        "funded_places_total": "25",
        "paid_places": "10",
        "passing_score_budget": "220",
        "passing_score_contract": "150",
        "consultations": "<p>Консультации по программе проводятся еженедельно по средам.</p>",
    },
    {
        "title": "Информационные системы и технологии",
        "edu_area": "09.03.02 Информационные системы и технологии",
        "edu_cost": "210000",
        "exam_subjects": ["Русский язык", "Математика (профильная)", "Физика"],
        "exam_details": {
            "Русский язык": ("1", "1"),
            "Математика (профильная)": ("1", "2"),
            "Физика": ("0", "3"),
        },
        "funded_place_types": ["Основные места в рамках КЦП"],
        "funded_place_counts": {"Основные места в рамках КЦП": "18"},
        "partners": ["ПАО «Ростелеком»"],
        "profiles": ["Информационные системы предприятия"],
        "professions": ["Аналитик данных"],
        "contacts": ["Приёмная комиссия ЮУрГУ"],
        "edu_form_value": "0",
        "branch_value": "0",
        "division_value": "3",
        "language_value": "0",
        "front_page_position_value": "1",  # 2
        "duration": "4 года",
        "funded_places_total": "20",
        "paid_places": "12",
        "passing_score_budget": "210",
        "passing_score_contract": "140",
        "consultations": "<p>Индивидуальные консультации по записи через приёмную комиссию.</p>",
    },
    {
        "title": "Экономика предприятий и организаций",
        "edu_area": "38.03.01 Экономика",
        "edu_cost": "195000",
        "exam_subjects": ["Русский язык", "Математика (профильная)", "Обществознание"],
        "exam_details": {
            "Русский язык": ("1", "1"),
            "Математика (профильная)": ("1", "2"),
            "Обществознание": ("1", "3"),
        },
        "funded_place_types": ["Особая квота", "Отдельная квота"],
        "funded_place_counts": {"Особая квота": "3", "Отдельная квота": "2"},
        "partners": ["Правительство Челябинской области"],
        "profiles": ["Экономика предприятий и организаций"],
        "professions": ["Экономист"],
        "contacts": ["Приёмная комиссия ЮУрГУ"],
        "edu_form_value": "1",  # заочная
        "branch_value": "0",
        "division_value": "2",  # Высшая школа экономики и управления
        "language_value": "0",
        "front_page_position_value": "2",  # 3
        "duration": "5 лет",
        "funded_places_total": "15",
        "paid_places": "30",
        "passing_score_budget": "200",
        "passing_score_contract": "120",
        "consultations": "<p>Консультации проводятся дистанционно по будням.</p>",
    },
    {
        "title": "Автоматизация технологических процессов и производств",
        "edu_area": "15.03.04 Автоматизация технологических процессов и производств",
        "edu_cost": "205000",
        "exam_subjects": ["Русский язык", "Математика (профильная)", "Физика"],
        "exam_details": {
            "Русский язык": ("1", "1"),
            "Математика (профильная)": ("1", "2"),
            "Физика": ("1", "3"),
        },
        "funded_place_types": ["Основные места в рамках КЦП", "Целевая квота"],
        "funded_place_counts": {"Основные места в рамках КЦП": "22", "Целевая квота": "8"},
        "partners": ["АО «Челябинский трубопрокатный завод»"],
        "profiles": ["Автоматизация производственных процессов"],
        "professions": ["Инженер-технолог"],
        "contacts": ["Приёмная комиссия ЮУрГУ"],
        "edu_form_value": "0",
        "branch_value": "2",  # Миасс
        "division_value": "8",  # Политехнический институт
        "language_value": "0",
        "front_page_position_value": "3",  # 4
        "duration": "4 года",
        "funded_places_total": "30",
        "paid_places": "8",
        "passing_score_budget": "190",
        "passing_score_contract": "110",
        "consultations": "<p>Консультации на площадке филиала в г. Миасс.</p>",
    },
    {
        "title": "Строительство",
        "edu_area": "08.03.01 Строительство",
        "edu_cost": "215000",
        "exam_subjects": ["Русский язык", "Математика (профильная)", "Физика"],
        "exam_details": {
            "Русский язык": ("1", "1"),
            "Математика (профильная)": ("1", "2"),
            "Физика": ("1", "3"),
        },
        "funded_place_types": ["Основные места в рамках КЦП"],
        "funded_place_counts": {"Основные места в рамках КЦП": "25"},
        "partners": ["АО «Челябинский трубопрокатный завод»"],
        "profiles": ["Промышленное и гражданское строительство"],
        "professions": ["Инженер-строитель"],
        "contacts": ["Приёмная комиссия ЮУрГУ"],
        "edu_form_value": "0",
        "branch_value": "0",
        "division_value": "0",  # Архитектурно-строительный институт
        "language_value": "0",
        "front_page_position_value": "4",  # 5
        "duration": "4 года",
        "funded_places_total": "28",
        "paid_places": "15",
        "passing_score_budget": "195",
        "passing_score_contract": "115",
        "consultations": "<p>Консультации по программе — очно на кафедре.</p>",
    },
    {
        "title": "Юриспруденция",
        "edu_area": "40.03.01 Юриспруденция",
        "edu_cost": "225000",
        "exam_subjects": ["Русский язык", "Обществознание", "Иностранный язык"],
        "exam_details": {
            "Русский язык": ("1", "1"),
            "Обществознание": ("1", "2"),
            "Иностранный язык": ("0", "3"),
        },
        "funded_place_types": ["Целевая квота"],
        "funded_place_counts": {"Целевая квота": "5"},
        "partners": ["Правительство Челябинской области"],
        "profiles": ["Гражданское право"],
        "professions": ["Юрист"],
        "contacts": ["Приёмная комиссия ЮУрГУ"],
        "edu_form_value": "2",  # очно-заочная
        "branch_value": "0",
        "division_value": "9",  # Юридический институт
        "language_value": "0",
        "front_page_position_value": "5",  # 6
        "duration": "4 года",
        "funded_places_total": "10",
        "paid_places": "40",
        "passing_score_budget": "230",
        "passing_score_contract": "160",
        "consultations": "<p>Консультации проводятся преподавателями юридического института.</p>",
    },
]


def test_reset_db(driver):
    login_page = WpLoginPage(driver)
    login_page.open()
    login_page.login(Config.wp_admin_login(), Config.wp_admin_password())

    reset_db_page = ResetDbPage(driver)
    reset_db_page.open()
    reset_db_page.assert_reset_db_button_visible()
    reset_db_page.click_reset_db()

    education_program_list_page = EducationProgramListPage(driver)
    education_program_list_page.open()
    education_program_list_page.assert_empty()


def test_fill_education_programs(driver):
    login_page = WpLoginPage(driver)
    login_page.open()
    login_page.login(Config.wp_admin_login(), Config.wp_admin_password())

    reset_db_page = ResetDbPage(driver)
    reset_db_page.open()
    reset_db_page.assert_reset_db_button_visible()
    reset_db_page.click_reset_db()

    term_page = TermPage(driver)
    for taxonomy, names in TAXONOMY_TERMS.items():
        term_page.open(taxonomy)
        for name in names:
            term_page.add_term(name)

    add_program_page = AddEducationProgramPage(driver)
    for program in PROGRAMS:
        add_program_page.open()
        add_program_page.fill_program(program)
        add_program_page.publish()

        # Таблицы "Вступительные испытания по типам" и "Бюджетные места"
        # рендерятся сервером только после первой публикации, поэтому детали
        # заполняются вторым проходом и требуют повторного сохранения.
        add_program_page.fill_exam_details(program["exam_details"])
        add_program_page.fill_funded_place_counts(program["funded_place_counts"])
        add_program_page.publish()

    education_program_list_page = EducationProgramListPage(driver)
    education_program_list_page.open()
    for program in PROGRAMS:
        education_program_list_page.assert_contains(program["title"])
