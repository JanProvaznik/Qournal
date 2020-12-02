from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtCore import Qt
import sys

from model.Models import Area

app = QApplication(sys.argv)
areas = []

class DefaultView(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.show()

    def renderAreas(self, event):
        pass



s = DefaultView()
app.exec_()

