from PyQt5.QtCore import QTimer
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit


class TypingTimeoutTimer(QTimer):
    def __init__(self, parent=None, typing_timeout=500):
        super().__init__(parent)
        self.setInterval(typing_timeout)
        self.setSingleShot(True)


class MyEdit(QTextEdit):
    typing_started = pyqtSignal()
    typing_stopped = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.typing_timeout = TypingTimeoutTimer(self)

        self.textChanged.connect(self.typing_timeout.start)
        self.textChanged.connect(self.typing_start)
        self.typing_timeout.timeout.connect(self.typing_stop)

    @pyqtSlot()
    def typing_start(self):
        self.typing_started.emit()

    @pyqtSlot()
    def typing_stop(self):
        self.typing_stopped.emit()


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel()
        self.edit = MyEdit()

        self.edit.typing_started.connect(self.set_typing)
        self.edit.typing_stopped.connect(self.set_not_typing)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.edit)
        self.setLayout(layout)

    @pyqtSlot()
    def set_typing(self):
        self.label.setText("typing")

    @pyqtSlot()
    def set_not_typing(self):
        self.label.setText("")


if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()
