from pathlib import Path
from classes.config import Config
from pages.wp_login.WpLoginPage import WpLoginPage
from pages.test.ResetDbPage import ResetDbPage
from pages.wp_admin.EducationProgramListPage import EducationProgramListPage
from pages.wp_admin.AddEducationProgramPage import AddEducationProgramPage
from pages.wp_admin.TermPage import TermPage
from fixtures.taxonomy_terms import TAXONOMY_TERMS
from fixtures.programs import PROGRAMS

EDU_AREA_NAME = "09.03.01 Информатика и вычислительная техника"
TAXONOMIES_WITH_IMAGE = {"partners", "professions", "contacts"}
TAXONOMIES_WITH_PDF = {"subjects_spo"}
LOGO_IMAGE_PATH = str(Path(__file__).parent / "fixtures" / "logo.png")
SPO_PDF_PATH = str(Path(__file__).parent / "fixtures" / "spo_template.pdf")


def test_reset_db(driver):
    login_page = WpLoginPage(driver)
    login_page.open()
    login_page.login(Config.wp_admin_login(), Config.wp_admin_password())

    reset_db_page = ResetDbPage(driver)
    reset_db_page.open()
    reset_db_page.assert_reset_db_button_visible()
    reset_db_page.click_reset_db()
    reset_db_page.assert_success_message_visible()

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
    reset_db_page.assert_success_message_visible()

    term_page = TermPage(driver)
    for taxonomy, terms in TAXONOMY_TERMS.items():
        term_page.taxonomy = taxonomy
        term_page.open()
        image_path = LOGO_IMAGE_PATH if taxonomy in TAXONOMIES_WITH_IMAGE else None
        pdf_path = SPO_PDF_PATH if taxonomy in TAXONOMIES_WITH_PDF else None
        for term in terms:
            if isinstance(term, dict):
                name = term["name"]
                description = term.get("description")
                content = term.get("content")
            else:
                name, description, content = term, None, None
            term_page.add_term(name, image_path=image_path, pdf_path=pdf_path, description=description, content=content)

    add_program_page = AddEducationProgramPage(driver)
    for program in PROGRAMS:
        add_program_page.open()
        add_program_page.fill_program(program)
        add_program_page.publish()
        add_program_page.fill_exam_details(program["exam_details"])
        add_program_page.fill_funded_place_counts(program["funded_place_counts"])
        add_program_page.fill_profile_details(program["profile_details"])
        add_program_page.publish()

    education_program_list_page = EducationProgramListPage(driver)
    education_program_list_page.open()
    for program in PROGRAMS:
        education_program_list_page.assert_contains(program["title"])
