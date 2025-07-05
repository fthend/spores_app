from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import QComboBox, QStyledItemDelegate, QSizePolicy
from PySide6.QtCore import Qt, QEvent, Signal


class MultiSelectComboBox(QComboBox):
    selection_changed = Signal()
    def __init__(self, items=None, parent=None):
        super().__init__(parent)
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self.lineEdit().setPlaceholderText("Выберите...")
        self.setInsertPolicy(QComboBox.NoInsert)
        self.setModel(QStandardItemModel(self))
        self.setItemDelegate(QStyledItemDelegate(self))
        self.closeOnLineEditClick = False
        self.view().viewport().installEventFilter(self)

        # Установка фильтра событий на lineEdit
        self.lineEdit().installEventFilter(self)

        if items:
            for item_text in items:
                self.addItem(item_text)
                item = self.model().item(self.count() - 1)
                item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                item.setData(Qt.Unchecked, Qt.CheckStateRole)

        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # self.setMaximumWidth(230)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        self.setMinimumWidth(230)
        self.setMaximumWidth(400)

        self.update_display()

        self.view().pressed.connect(self.handle_item_pressed)

    def eventFilter(self, obj, event):
        if obj == self.lineEdit() and event.type() == QEvent.MouseButtonRelease:
            if self.closeOnLineEditClick:
                self.hidePopup()
            else:
                self.showPopup()
            return True
        return False

    def showPopup(self):
        super().showPopup()
        self.closeOnLineEditClick = True

    def hidePopup(self):
        super().hidePopup()
        self.startTimer(100)

    def timerEvent(self, event):
        self.killTimer(event.timerId())
        self.closeOnLineEditClick = False
    def handle_item_pressed(self, index):
        item = self.model().itemFromIndex(index)
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)
        self.update_display()
        self.selection_changed.emit()

    def update_display(self):
        selected = [self.model().item(i).text()
                    for i in range(self.count())
                    if self.model().item(i).checkState() == Qt.Checked]
        self.lineEdit().setText("; ".join(selected))

    def selectedItems(self):
        return [self.model().item(i).text()
                for i in range(self.count())
                if self.model().item(i).checkState() == Qt.Checked]

    def clear_selection(self):
        for i in range(self.count()):
            item = self.model().item(i)
            item.setCheckState(Qt.Unchecked)
        self.update_display()
        self.selection_changed.emit()
