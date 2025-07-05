import sys
from PySide6.QtWidgets import QApplication

from db.db_service import ensure_backup_exists
from logic.main_window_logic import MainApp
from qt_material import apply_stylesheet

def main():
    app = QApplication(sys.argv)

    apply_stylesheet(app, theme="white_light_blue.xml")
    ensure_backup_exists()
    window = MainApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()


