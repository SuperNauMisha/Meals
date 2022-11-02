import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QListView, QComboBox, QPushButton, QFormLayout, QGroupBox, QMessageBox
import sqlite3
import main

class PickUp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('pick_up.ui', self)
        self.connection = sqlite3.connect("Meals.db")
        self.cur = self.connection.cursor()
        self.all_ingredients = []
        self.all_dishes = []
        for ingr in self.cur.execute("""SELECT name FROM ingredients""").fetchall():
            self.all_ingredients.append(ingr[0])
        for dish in self.cur.execute("""SELECT name FROM dishes""").fetchall():
            self.all_dishes.append(dish[0])
        self.ingredientsLabelList = []
        self.delIngButtonList = []
        self.noGirdLoad = True
        self.ok.clicked.connect(self.appendIngredient)
        self.back.clicked.connect(self.backToMain)
        self.search.clicked.connect(self.searchDish)
        self.comboBox.addItems(self.all_ingredients)
        print(self.all_ingredients)
        print(self.all_dishes)

    def appendIngredient(self):
        if self.comboBox.currentText().lower() in [i.lower() for i in self.all_ingredients]:
            if self.noGirdLoad:
                self.formLayout = QFormLayout()
                self.groupBox = QGroupBox()
                self.formLayout.setContentsMargins(10, 10, 10, 10)
                self.ingredientsLabelList.append(QLabel(self.comboBox.currentText()))
                but = QPushButton("Удалить")
                but.clicked.connect(self.delIngredient)
                self.delIngButtonList.append(but)
                self.formLayout.addRow(self.ingredientsLabelList[-1], self.delIngButtonList[-1])
                self.groupBox.setLayout(self.formLayout)
                self.ingScroll.setWidget(self.groupBox)
                self.ingScroll.setWidgetResizable(True)
            else:
                if self.comboBox.currentText().lower() not in [i.text().lower() for i in self.ingredientsLabelList]:
                    self.ingredientsLabelList.append(QLabel(self.comboBox.currentText()))
                    but = QPushButton("Удалить")
                    but.clicked.connect(self.delIngredient)
                    self.delIngButtonList.append(but)
                    self.formLayout.addRow(self.ingredientsLabelList[-1], self.delIngButtonList[-1])
                else:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Сообщение")
                    msg.setText("Этот ингридент уже есть в списке")
                    msg.exec_()
            self.noGirdLoad = False
        else:
            msg = QMessageBox(self)
            msg.setWindowTitle("Сообщение")
            msg.setText('Этого ингридента не существует! \nВы можете добавить собственный ингридиент \nво вкладке "Создать ингридиент"')
            msg.exec_()

    def delIngredient(self):
        index = self.delIngButtonList.index(self.sender())
        self.delIngButtonList[index].deleteLater()
        del self.delIngButtonList[index]
        self.ingredientsLabelList[index].deleteLater()
        del self.ingredientsLabelList[index]

    def searchDish(self):
        selected_ingredients = [i.text().lower() for i in self.ingredientsLabelList]
        picked_dishes = []
        print(selected_ingredients)
        for d_id in self.cur.execute("""SELECT id FROM dishes""").fetchall():
            there_is = True
            for i_id in self.cur.execute("""SELECT ingridient_id FROM conections
                        WHERE dish_id = ?""", (d_id[0],)).fetchall():
                if self.cur.execute("""SELECT name FROM ingredients
                        WHERE id = ?""", (i_id[0],)).fetchall()[0][0].lower() not in selected_ingredients:
                    there_is = False
                    break
            if there_is:
                picked_dishes.append(self.cur.execute("""SELECT name FROM dishes
                        WHERE id = ?""", (d_id[0],)).fetchall()[0][0])
        print(picked_dishes)

    def backToMain(self):
        self.menu = main.Menu()
        self.menu.show()
        self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PickUp()
    ex.show()
    sys.exit(app.exec_())
