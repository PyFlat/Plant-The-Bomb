from PySide6.QtWidgets import QDialog, QLabel, QMessageBox, QVBoxLayout
class KeybindDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.label = QLabel("Please press the new keybind.", self)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setWindowTitle("Keybind Instruction")

class BasicDialog(QMessageBox):
    def __init__(self, parent=None, title:str="", message:str="", icon:int=None):
        super().__init__(parent=parent)
        self.setWindowTitle(title)
        self.setText(message)
        self.setIcon(QMessageBox.Critical)
        self.exec()

