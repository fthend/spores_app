import os
import sys

from PySide6.QtGui import QShowEvent, QIcon
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLineEdit, QLabel, QPushButton, QTableWidget,
    QToolBar, QTabWidget, QTabBar, QAbstractItemView, QSizePolicy
)
from PySide6.QtCore import Qt
from qt_material import apply_stylesheet

from ui.ui_help_tab import HelpTab
from ui.ui_search_panel import SearchPanel

class MainWindow(QMainWindow):
    def __init__(self, options_data=None):
        super().__init__()
        self.setWindowTitle("Каталог миоспор позднего палеозоя")
        # self.setMinimumSize(1000, 600)
        self.resize(1000, 600)
        icon_path = resource_path("ui/images/icon.svg")
        self.setWindowIcon(QIcon(icon_path))

        self.themes = [
            "white_light_blue.xml",
            "dark_blue.xml",
        ]
        self.current_theme = 0

        # Главный виджет с вкладками
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)

        self.create_main_tab(options_data)
        self.setCentralWidget(self.tab_widget)

        toolbar = QToolBar("Навигация")
        self.addToolBar(Qt.TopToolBarArea, toolbar)

        theme_toggle_btn = QPushButton("Переключить тему")
        theme_toggle_btn.clicked.connect(self.toggle_theme)
        toolbar.addWidget(theme_toggle_btn)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        toolbar.addWidget(spacer)

        help_btn = QPushButton("Справка")
        help_btn.clicked.connect(self.open_help_tab)
        toolbar.addWidget(help_btn)


    def create_main_tab(self, options_data=None):
        main_tab = QWidget()
        main_layout = QHBoxLayout(main_tab)
        self.search_panel = SearchPanel(options_data=options_data)
        main_layout.addWidget(self.search_panel, 1)

        right_layout = QVBoxLayout()

        # Панель с поиском и кнопкой добавления
        top_panel = QHBoxLayout()

        # Поиск
        search_bar_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск...")
        search_icon = QLabel("🔍")
        search_bar_layout.addWidget(search_icon)
        search_bar_layout.addWidget(self.search_input)
        top_panel.addLayout(search_bar_layout, stretch=1)

        # Группа кнопок действий
        btn_group = QHBoxLayout()
        self.add_genus_btn = QPushButton("Добавить род")
        self.export_btn = QPushButton("Экспорт")

        self.edit_btn = QPushButton("Изменить")
        self.edit_btn.setEnabled(False)

        self.delete_btn = QPushButton("Удалить")
        self.delete_btn.setEnabled(False)


        btn_group.addWidget(self.add_genus_btn)
        btn_group.addWidget(self.export_btn)
        btn_group.addWidget(self.edit_btn)
        btn_group.addWidget(self.delete_btn)

        top_panel.addLayout(btn_group)

        right_layout.addLayout(top_panel)

        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels([
            "Название рода",
            "Синонимы",
            "Инфратурма"
        ])
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        # Настройка выделения строк
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)

        # Сигнал изменения выделения
        self.table.itemSelectionChanged.connect(self.update_buttons_state)

        right_layout.addWidget(self.table)

        main_layout.addLayout(right_layout, 2)
        self.tab_widget.addTab(main_tab, "Главная")
        self.tab_widget.tabBar().setTabButton(0, QTabBar.RightSide, None)

    def update_buttons_state(self):
        has_selection = len(self.table.selectedItems()) > 0
        self.edit_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)
    def add_genus_tab(self, detail_tab, tab_name):
        for i in range(1, self.tab_widget.count()):
            if self.tab_widget.tabText(i) == tab_name:
                self.tab_widget.setCurrentIndex(i)
                return
        index = self.tab_widget.addTab(detail_tab, tab_name)
        self.tab_widget.setCurrentIndex(index)

    def close_tab(self, index):
        if index != 0:
            self.tab_widget.removeTab(index)

    def showEvent(self, event: QShowEvent):
        super().showEvent(event)
        self.adjust_column_widths()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.adjust_column_widths()

    def adjust_column_widths(self):
        total_width = self.table.viewport().width()
        col_count = self.table.columnCount()

        col_width = total_width // col_count

        for i in range(col_count):
            self.table.setColumnWidth(i, col_width)

    def toggle_theme(self):
        self.current_theme = (self.current_theme + 1) % len(self.themes)
        apply_stylesheet(self.window(), theme=self.themes[self.current_theme])

    def open_help_tab(self):
        tab_name = "Справка"
        for i in range(1, self.tab_widget.count()):
            if self.tab_widget.tabText(i) == tab_name:
                self.tab_widget.setCurrentIndex(i)
                return
        help_tab = HelpTab(self)
        index = self.tab_widget.addTab(help_tab, tab_name)
        self.tab_widget.setCurrentIndex(index)

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)