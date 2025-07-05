import os
import shutil
from PySide6.QtWidgets import QMessageBox
from config import get_db_path

# Сброс БД до резервной копии
def reset_database(parent_widget=None):
    db_path = get_db_path()
    backup_path = os.path.join(os.path.dirname(db_path), 'miospores_backup.db')

    try:
        # Проверяем существование резервной копии
        if not os.path.exists(backup_path):
            QMessageBox.critical(parent_widget, "Ошибка",
                                 "Резервная копия базы данных не найдена!")
            return False
        from db.session import dispose_engine
        dispose_engine()

        if os.path.exists(db_path):
            os.remove(db_path)
        shutil.copy2(backup_path, db_path)

        return True

    except Exception as e:
        QMessageBox.critical(parent_widget, "Ошибка",
                             f"Не удалось восстановить базу данных:\n{str(e)}")
        return False

# Создает резервную копию при первом запуске, если ее нет
def ensure_backup_exists():
    db_path = get_db_path()
    backup_path = os.path.join(os.path.dirname(db_path), 'miospores_backup.db')

    if not os.path.exists(backup_path) and os.path.exists(db_path):
        shutil.copy2(db_path, backup_path)