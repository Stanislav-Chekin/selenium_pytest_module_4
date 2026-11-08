from unittest.mock import Mock
# Импортируем наш класс из файла resource_manager.py
from resource_manager import ResourceManager


def test_resource_manager_update():
    # 1. Создаем МОК (фальшивую базу данных)
    mock_db = Mock()

    # 2. Инъекция зависимости: передаем мок в класс
    manager = ResourceManager(connection=mock_db)

    # 3. Вызываем метод, который должен дернуть базу
    manager.update()

    # 4. Проверяем (Assert), что методы мока были вызваны
    mock_db.connect.assert_called_once()
    mock_db.update_database.assert_called_once()

# Запустить pytest lesson_materials/test_dependency_injection.py -v -s
