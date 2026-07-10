from pages.education_program.EducationProgramArchivePage import EducationProgramArchivePage


def test_education_program_filters(driver):
    page = EducationProgramArchivePage(driver)
    page.open()
    page.assert_has_programs()

    initial_count = page.get_program_count()

    # 1 Направление подготовки
    page.select_filter_direction("09.03.01 Информатика и вычислительная техника")
    page.click_apply_filters()
    page.wait_for_filters_applied()

    filtered_count = page.get_program_count()
    assert filtered_count > 0
    assert filtered_count <= initial_count

    titles = page.get_program_titles()
    assert any("09.03.01" in title for title in titles)

    page.click_reset_filters()
    page.wait_for_filters_applied()

    reset_count = page.get_program_count()
    assert reset_count == initial_count

    # 2 Вступительные испытания
    page.select_filter_exam_subjects([
        "Русский язык",
        "Математика (профильная)",
        "Информатика и ИКТ"
    ])
    page.click_apply_filters()
    page.wait_for_filters_applied()

    exam_filtered_count = page.get_program_count()
    assert exam_filtered_count > 0
    assert exam_filtered_count <= initial_count

    page.click_reset_filters()
    page.wait_for_filters_applied()

    # 3 Форма обучения
    page.select_filter_form("очная")
    page.click_apply_filters()
    page.wait_for_filters_applied()

    form_filtered_count = page.get_program_count()
    assert form_filtered_count > 0

    page.click_reset_filters()
    page.wait_for_filters_applied()

    # 4 Уровень образования
    page.select_filter_education_level("Бакалавриат")
    page.click_apply_filters()
    page.wait_for_filters_applied()

    level_filtered_count = page.get_program_count()
    if level_filtered_count > 0:
        assert level_filtered_count <= initial_count

    page.click_reset_filters()
    page.wait_for_filters_applied()

    # 5 Подразделение
    page.select_filter_division("Юридический институт")
    page.click_apply_filters()
    page.wait_for_filters_applied()

    division_filtered_count = page.get_program_count()
    assert division_filtered_count > 0
    assert division_filtered_count <= initial_count

    titles = page.get_program_titles()
    assert len(titles) == division_filtered_count

    page.click_reset_filters()
    page.wait_for_filters_applied()

    final_count = page.get_program_count()
    assert final_count == initial_count


def test_education_program_multiple_filters(driver):
    """Тест проверяет работу нескольких фильтров одновременно"""
    page = EducationProgramArchivePage(driver)
    page.open()
    page.assert_has_programs()

    initial_count = page.get_program_count()

    # 1 Направление + Форма обучения
    page.select_filter_direction("09.03.01 Информатика и вычислительная техника")
    page.select_filter_form("очная")
    page.click_apply_filters()
    page.wait_for_filters_applied()

    combo1_count = page.get_program_count()
    assert combo1_count > 0
    assert combo1_count <= initial_count

    titles = page.get_program_titles()
    assert any("09.03.01" in title for title in titles)

    page.click_reset_filters()
    page.wait_for_filters_applied()

    # 2 Вступительные испытания + Подразделение
    page.select_filter_exam_subjects([
        "Русский язык",
        "Математика (профильная)",
        "Информатика и ИКТ"
    ])
    page.select_filter_division("Высшая школа электроники и компьютерных наук")
    page.click_apply_filters()
    page.wait_for_filters_applied()

    combo2_count = page.get_program_count()
    assert combo2_count > 0
    assert combo2_count <= initial_count

    page.click_reset_filters()
    page.wait_for_filters_applied()

    # 3 Направление + Вступительные испытания + Форма обучения
    page.select_filter_direction("38.03.01 Экономика")
    page.select_filter_exam_subjects([
        "Русский язык",
        "Математика (профильная)",
        "Обществознание"
    ])
    page.select_filter_form("очная")
    page.click_apply_filters()
    page.wait_for_filters_applied()

    combo3_count = page.get_program_count()
    assert combo3_count > 0
    assert combo3_count <= initial_count

    titles = page.get_program_titles()
    assert any("38.03.01" in title for title in titles)

    page.click_reset_filters()
    page.wait_for_filters_applied()

    # 4 Все доступные фильтры
    page.select_filter_direction("09.03.01 Информатика и вычислительная техника")
    page.select_filter_exam_subjects([
        "Русский язык",
        "Математика (профильная)",
        "Информатика и ИКТ"
    ])
    page.select_filter_form("очная")
    page.select_filter_division("Высшая школа электроники и компьютерных наук")
    page.click_apply_filters()
    page.wait_for_filters_applied()

    combo4_count = page.get_program_count()
    assert combo4_count > 0
    assert combo4_count <= combo1_count

    titles = page.get_program_titles()
    assert any("09.03.01" in title for title in titles)

    page.click_reset_filters()
    page.wait_for_filters_applied()

    final_count = page.get_program_count()
    assert final_count == initial_count

