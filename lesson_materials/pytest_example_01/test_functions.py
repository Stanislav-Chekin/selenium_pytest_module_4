# pytest ОБНАРУЖИТ эту функцию (начинается с test_)
def test_addition_success():
    assert 1 + 1 == 2


# pytest ОБНАРУЖИТ эту функцию (начинается с test_)
def test_subtraction_success():
    assert 5 - 3 == 2


# pytest ИГНОРИРУЕТ эту функцию (не начинается с test_)
def helper_calculate_margin(value):
    return value * 1.2


# pytest ОБНАРУЖИТ эту функцию, внутри которой используется helper
def test_margin_calculation():
    result = helper_calculate_margin(10)
    assert result == 12

# Запустить pytest lesson_materials/pytest_example_01/test_functions.py -v
