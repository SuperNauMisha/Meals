import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QListView, QComboBox, QPushButton, QFormLayout, QGroupBox, QMessageBox
import main
import sqlite3


class CreateIngridient(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('create_ingridient.ui', self)
        self.connection = sqlite3.connect("Meals.db")
        self.cur = self.connection.cursor()
        self.noGirdLoad = True
        self.all_ingredients = []
        self.ingredientsLabelList = []
        self.delIngButtonList = []
        for ingr in self.cur.execute("""SELECT name FROM ingredients""").fetchall():
            self.all_ingredients.append(ingr[0])
        max_id = max([ing[0] for ing in self.cur.execute("""SELECT id FROM ingredients""").fetchall()])
        print(max_id)
        self.loadIngridients()

    def loadIngridients(self):
        if self.noGirdLoad:
            self.formLayout = QFormLayout()
            self.groupBox = QGroupBox()
            self.formLayout.setContentsMargins(10, 10, 10, 10)
            self.groupBox.setLayout(self.formLayout)
            self.ingScroll.setWidget(self.groupBox)
            self.ingScroll.setWidgetResizable(True)
            self.noGirdLoad = False
        for ing in self.all_ingredients:
            print(ing)
            self.ingredientsLabelList.append(QLabel(ing))
            but = QPushButton("Удалить")
            but.clicked.connect(self.delIngredient)
            self.delIngButtonList.append(but)
            self.formLayout.addRow(self.ingredientsLabelList[-1], self.delIngButtonList[-1])

    def appendIngredient(self):
        print(1)
        if self.lineEdit.text().lower() not in [i.lower() for i in self.all_ingredients]:
            print(2)
            self.ingredientsLabelList.append(QLabel(self.lineEdit.text()))
            print(3)
            but = QPushButton("Удалить")
            but.clicked.connect(self.delIngredient)
            self.delIngButtonList.append(but)
            self.formLayout.addRow(self.ingredientsLabelList[-1], self.delIngButtonList[-1])
        else:
            msg = QMessageBox(self)
            msg.setWindowTitle("Сообщение")
            msg.setText("Этот ингридент уже есть в списке")
            msg.exec_()

    def delIngredient(self):
        pass

    def backToMain(self):
        self.menu = main.Menu()
        self.menu.show()
        self.hide()
