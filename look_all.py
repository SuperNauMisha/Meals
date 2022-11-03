from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QListView, QComboBox, QPushButton, QFormLayout, QGroupBox, QMessageBox
import sqlite3
import main


class LookAll(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('look_all_dishes.ui', self)
        self.connection = sqlite3.connect("Meals.db")
        self.cur = self.connection.cursor()
        self.all_dishes_id = []
        for dish_id in self.cur.execute("""SELECT id FROM dishes""").fetchall():
            self.all_dishes_id.append(dish_id[0])

        self.ButtonList = []
        self.id_list = []
        self.noGirdLoad = True
        self.back.clicked.connect(self.backToMain)
        self.search.clicked.connect(self.loadIngridients)
        self.loadIngridients()

    def loadIngridients(self):
        if self.noGirdLoad:
            self.formLayout = QFormLayout()
            self.groupBox = QGroupBox()
            self.formLayout.setContentsMargins(10, 10, 10, 10)
            self.groupBox.setLayout(self.formLayout)
            self.dishScroll.setWidget(self.groupBox)
            self.dishScroll.setWidgetResizable(True)
            self.noGirdLoad = False
        for but in self.ButtonList:
            but.deleteLater()
        self.ButtonList = []
        self.id_list = []
        for dish_id in self.all_dishes_id:
            name = self.cur.execute("""SELECT name FROM dishes
                        WHERE id = ?""", (dish_id,)).fetchall()[0][0]
            if self.dishLine.text().lower() in name.lower():
                but = QPushButton(name)
                self.id_list.append(dish_id)
                but.clicked.connect(self.lookDish)
                self.ButtonList.append(but)
                self.formLayout.addRow(self.ButtonList[-1])

    def lookDish(self):
        index = self.ButtonList.index(self.sender())
        id = self.id_list[index]
        msg = QMessageBox(self)
        msg.setStyleSheet("background-color: rgb(255, 201, 60);")
        msg.setWindowTitle(self.sender().text() + ' ' + str(self.cur.execute("""SELECT mass FROM dishes
                                    WHERE id = ?""", (id,)).fetchall()[0][0]) + " г")
        text = ''
        for ing_id in self.cur.execute("""SELECT ingridient_id FROM conections
                                WHERE dish_id = ?""", (id,)).fetchall():
            text += self.cur.execute("""SELECT name FROM ingredients
                                WHERE id = ?""", (ing_id[0],)).fetchall()[0][0]
            text += " "
            text += str(self.cur.execute("""SELECT mass FROM conections
                                WHERE ingridient_id = ?""", (ing_id[0],)).fetchall()[0][0])
            text += " г"
            text += "\n"
        msg.setText(text)
        msg.exec_()

    def backToMain(self):
        self.cur.close()
        self.menu = main.Menu()
        self.menu.show()
        self.hide()
