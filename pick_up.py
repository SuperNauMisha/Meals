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
        self.idNeedDishes = []
        self.dishButtonList = []
        self.noGirdLoad = True
        self.noDishGirdLoad = True
        self.ok.clicked.connect(self.appendIngredient)
        self.back.clicked.connect(self.backToMain)
        self.search.clicked.connect(self.searchDish)
        self.comboBox.addItems(self.all_ingredients)

    def appendIngredient(self):
        if self.comboBox.currentText().lower() in [i.lower() for i in self.all_ingredients]:
            if self.noGirdLoad:
                self.formLayout = QFormLayout()
                self.groupBox = QGroupBox()
                self.formLayout.setContentsMargins(10, 10, 10, 10)
                self.groupBox.setLayout(self.formLayout)
                self.ingScroll.setWidget(self.groupBox)
                self.ingScroll.setWidgetResizable(True)
                self.noGirdLoad = False
            if self.comboBox.currentText().lower() not in [i.text().lower() for i in self.ingredientsLabelList]:
                self.ingredientsLabelList.append(QLabel(self.comboBox.currentText()))
                but = QPushButton("Удалить")
                but.clicked.connect(self.delIngredient)
                self.delIngButtonList.append(but)
                self.formLayout.addRow(self.ingredientsLabelList[-1], self.delIngButtonList[-1])
            else:
                msg = QMessageBox(self)
                msg.setStyleSheet("background-color: rgb(255, 201, 60);")
                msg.setWindowTitle("Сообщение")
                msg.setText("Этот ингридент уже есть в списке")
                msg.exec_()

        else:
            msg = QMessageBox(self)
            msg.setStyleSheet("background-color: rgb(255, 201, 60);")
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
        for d_id in self.cur.execute("""SELECT id FROM dishes""").fetchall():
            there_is = True
            for i_id in self.cur.execute("""SELECT ingridient_id FROM conections
                        WHERE dish_id = ?""", (d_id[0],)).fetchall():
                if self.cur.execute("""SELECT name FROM ingredients
                        WHERE id = ?""", (i_id[0],)).fetchall()[0][0].lower() not in selected_ingredients:
                    there_is = False
                    break
            if there_is:
                picked_dishes.append(d_id[0])
        if self.noDishGirdLoad:
            self.dishFormLayout = QFormLayout()
            self.dishGroupBox = QGroupBox()
            self.dishFormLayout.setContentsMargins(10, 10, 10, 10)
            self.dishGroupBox.setLayout(self.dishFormLayout)
            self.disScroll.setWidget(self.dishGroupBox)
            self.disScroll.setWidgetResizable(True)
            self.noDishGirdLoad = False
        for but in self.dishButtonList:
            but.deleteLater()
        self.dishButtonList = []
        for d_id in picked_dishes:
            but = QPushButton(self.cur.execute("""SELECT name FROM dishes
                    WHERE id = ?""", (d_id,)).fetchall()[0][0])
            but.clicked.connect(self.openDish)
            self.idNeedDishes.append(d_id)
            self.dishButtonList.append(but)
            self.dishFormLayout.addRow(self.dishButtonList[-1])


    def openDish(self):
        dishID = self.idNeedDishes[self.dishButtonList.index(self.sender())]
        msg = QMessageBox(self)
        msg.setStyleSheet("background-color: rgb(255, 201, 60);")
        msg.setWindowTitle(self.sender().text() + ' ' + str(self.cur.execute("""SELECT mass FROM dishes
                            WHERE id = ?""", (dishID,)).fetchall()[0][0]) + " г")
        text = ''
        for ing_id in self.cur.execute("""SELECT ingridient_id FROM conections
                        WHERE dish_id = ?""", (dishID,)).fetchall():
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
        self.menu = main.Menu()
        self.menu.show()
        self.hide()
