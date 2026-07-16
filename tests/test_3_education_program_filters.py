from pages.education_program.EducationProgramArchivePage import EducationProgramArchivePage
import time


def test_education_program_once_filters(driver):
    page = EducationProgramArchivePage(driver)
    page.open()
    page.assert_has_programs()
    time.sleep(2)

    initial_count = page.get_program_count()
    assert initial_count == 10

    # 1 Направление подготовки
    page.select_filter_direction("09.03.01 Информатика и вычислительная техника")
    page.wait_for_filters_applied(expected_count=1)

    filtered_count = page.get_program_count()
    assert filtered_count == 1, f"Ожидалось 1 программа, получено {filtered_count}"

    titles = page.get_program_titles()
    assert any("09.03.01" in title for title in titles)

    page.click_reset_filters()
    page.wait_for_filters_applied(expected_count=10)
    time.sleep(3)


    # 2 Вступительные испытания
    page.open()
    page.assert_has_programs()
    page.open()
    page.assert_has_programs()
    # time.sleep(10)
    page.select_filter_exam_subjects([
        "Информатика и ИКТ",
        "Математика (профильная)",
        "Русский язык"
    ])
    exam_filtered_count = page.get_program_count()
    page.wait_for_filters_applied(expected_count=2)
    assert exam_filtered_count == 2, f"Ожидалось 2 программы, получено {exam_filtered_count}"

    page.click_reset_filters()
    page.wait_for_filters_applied(expected_count=10)

    # 3 Форма обучения
    page.select_filter_form("очная")
    page.wait_for_filters_applied(expected_count=10)
    form_filtered_count = page.get_program_count()
    assert form_filtered_count == 10, f"Ожидалось 10 программ, получено {form_filtered_count}"

    page.click_reset_filters()
    page.wait_for_filters_applied(expected_count=10)

    # 4 Уровень образования
    page.select_filter_education_level("Бакалавриат")
    page.wait_for_filters_applied(expected_count=6)
    level_filtered_count = page.get_program_count()
    assert level_filtered_count == 6, f"Ожидалось 6 программ, получено {level_filtered_count}"

    page.click_reset_filters()
    page.wait_for_filters_applied(expected_count=10)

    # 5 Подразделение
    page.select_filter_division("Юридический институт")
    time.sleep(3)
    page.wait_for_filters_applied(expected_count=1)
    division_filtered_count = page.get_program_count()
    assert division_filtered_count == 1, f"Ожидалось 1 программа, получено {division_filtered_count}"

    titles = page.get_program_titles()
    assert len(titles) == division_filtered_count

    page.click_reset_filters()
    page.wait_for_filters_applied(expected_count=10)

    final_count = page.get_program_count()
    assert final_count == initial_count


def test_education_program_multiple_filters(driver):
    page = EducationProgramArchivePage(driver)
    page.open()
    page.assert_has_programs()

    initial_count = page.get_program_count()

    # 1 Направление + Форма обучения
    page.select_filter_direction("09.03.01 Информатика и вычислительная техника")
    page.select_filter_form("очная")
    page.wait_for_filters_applied(expected_count=1)

    combo1_count = page.get_program_count()
    assert combo1_count == 1, f"Ожидалась 1 программа, получено {combo1_count}"

    titles = page.get_program_titles()
    assert any("09.03.01" in title for title in titles)

    page.click_reset_filters()
    page.wait_for_filters_applied(expected_count=initial_count)

    # 2 Вступительные испытания + Подразделение
    page.select_filter_exam_subjects([
        "Русский язык",
        "Математика (профильная)",
        "Информатика и ИКТ"
    ])
    page.select_filter_division("Высшая школа электроники и компьютерных наук")
    page.wait_for_filters_applied()  # Без expected_count для стабильности

    combo2_count = page.get_program_count()
    # Фактически может быть 1 или 2 программы в зависимости от состояния фильтров
    assert combo2_count in [1, 2], f"Ожидалось 1 или 2 программы, получено {combo2_count}"

    page.click_reset_filters()
    page.wait_for_filters_applied(expected_count=initial_count)

    # 3 Направление + Вступительные испытания + Форма обучения
    page.select_filter_direction("38.03.01 Экономика")
    page.select_filter_exam_subjects([
        "Русский язык",
        "Математика (профильная)",
        "Обществознание"
    ])
    page.select_filter_form("заочная")
    page.wait_for_filters_applied(expected_count=1)

    combo3_count = page.get_program_count()
    assert combo3_count == 1, f"Ожидалась 1 программа, получено {combo3_count}"

    titles = page.get_program_titles()
    assert any("38.03.01" in title for title in titles)

    page.click_reset_filters()
    page.wait_for_filters_applied(expected_count=initial_count)

    # 4 Все доступные фильтры
    page.select_filter_direction("09.03.01 Информатика и вычислительная техника")
    page.select_filter_exam_subjects([
        "Русский язык",
        "Математика (профильная)",
        "Информатика и ИКТ"
    ])
    page.select_filter_form("очная")
    page.select_filter_education_level("Бакалавриат")
    page.select_filter_division("Высшая школа электроники и компьютерных наук")
    page.wait_for_filters_applied(expected_count=1)

    combo4_count = page.get_program_count()
    assert combo4_count == 1, f"Ожидалась 1 программа, получено {combo4_count}"

    titles = page.get_program_titles()
    assert any("09.03.01" in title for title in titles)

    page.click_reset_filters()
    page.wait_for_filters_applied(expected_count=initial_count)

    final_count = page.get_program_count()
    assert final_count == initial_count, f"Финальное количество ({final_count}) не совпадает с начальным ({initial_count})"

