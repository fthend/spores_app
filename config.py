# DATABASE_URL = "sqlite:///C:/Мария/Учеба/Диплом/miospore_data/db/miospores.db"

# DATABASE_URL = "sqlite:///miospores.db"

import os
import sys

# Возвращает правильный путь к БД в EXE или из исходного кода
def get_db_path():
    if getattr(sys, 'frozen', False):
        # Если приложение 'заморожено' в EXE
        base_dir = sys._MEIPASS
    else:
        # При обычном запуске из кода
        # base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        base_dir = ""
    return os.path.join(base_dir, 'miospores.db')


DATABASE_URL = f"sqlite:///{get_db_path()}"