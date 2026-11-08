class ResourceManager:
    def __init__(self, connection):
        # Мы НЕ создаем подключение здесь. Мы принимаем его "снаружи" (инъекция)
        self.connection = connection

    def set_db_connection(self, connection):
        self.connection = connection

    def update(self): # Убрали connection отсюда, он уже есть в self
        # self.connection = DBConnection() # ТАК ДЕЛАТЬ НЕЛЬЗЯ (жесткая связь)
        self.connection.connect()
        print("Do something...")
        self.connection.update_database()
# Переименован и исправлен из Dependency Injection the simplest example.py в resource_manager.py
# + добавлен файл test_dependency_injection в папку lesson_materials

