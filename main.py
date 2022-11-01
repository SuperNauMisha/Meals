import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QListView, QComboBox, QPushButton, QFormLayout, QGroupBox, QMessageBox
import sqlite3
import pickUp


class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_menu.ui', self)
        self.pickUpMeal.clicked.connect(self.pickUp)
        self.connection = sqlite3.connect("Meals.db")
        self.cur = self.connection.cursor()
        self.all_ingredients = []
        self.all_dishes = []
        for ingr in self.cur.execute("""SELECT name FROM ingredients""").fetchall():
            self.all_ingredients.append(ingr[0])
        for dish in self.cur.execute("""SELECT name FROM dishes""").fetchall():
            self.all_dishes.append(dish[0])


    def pickUp(self):
        pickUp.PickUp()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Menu()
    ex.show()
    sys.exit(app.exec_())
