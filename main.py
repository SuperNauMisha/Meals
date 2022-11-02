import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QListView, QComboBox, QPushButton, QFormLayout, QGroupBox, QMessageBox
import pick_up


class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_menu.ui', self)
        self.pickUpMeal.clicked.connect(self.pickUp)

    def pickUp(self):
        self.pickup = pick_up.PickUp()
        self.pickup.show()
        self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Menu()
    ex.show()
    sys.exit(app.exec_())
