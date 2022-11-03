from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QListView, QComboBox, QPushButton, QFormLayout, QGroupBox, QMessageBox
import sqlite3
import main


class CreateIngridient(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('create_ingridient.ui', self)
        self.ok.clicked.connect(self.appendIngredient)
        self.back.clicked.connect(self.backToMain)
        self.connection = sqlite3.connect("Meals.db")
        self.cur = self.connection.cursor()
        self.noGirdLoad = True
        self.all_ingredients_id = []
        self.all_ingredients = []
        self.ingredientsLabelList = []
        self.id_list = []
        self.delIngButtonList = []
        for ingr_id in self.cur.execute("""SELECT id FROM ingredients""").fetchall():
            self.all_ingredients_id.append(ingr_id[0])
        for ingr in self.cur.execute("""SELECT name FROM ingredients""").fetchall():
            self.all_ingredients.append(ingr[0])
        self.max_id = max(self.all_ingredients_id)
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
        for ing_id in self.all_ingredients_id:
            self.ingredientsLabelList.append(QLabel(self.cur.execute("""SELECT name FROM ingredients
                        WHERE id = ?""", (ing_id,)).fetchall()[0][0]))
            but = QPushButton("Удалить")
            but.setStyleSheet("background-color: rgb(255, 111, 60);")
            but.clicked.connect(self.delIngredient)
            self.delIngButtonList.append(but)
            self.id_list.append(ing_id)
            self.formLayout.addRow(self.ingredientsLabelList[-1], self.delIngButtonList[-1])

    def appendIngredient(self):
        if self.lineEdit.text().lower() not in [i.lower() for i in self.all_ingredients]:
            self.ingredientsLabelList.append(QLabel(self.lineEdit.text()))
            but = QPushButton("Удалить")
            but.setStyleSheet("background-color: rgb(255, 111, 60);")
            but.clicked.connect(self.delIngredient)
            self.delIngButtonList.append(but)
            self.max_id += 1
            self.id_list.append(self.max_id)
            self.all_ingredients_id.append(self.max_id)
            self.all_ingredients.append(self.lineEdit.text())
            sqlite_insert_with_param = """INSERT INTO ingredients
                              (id,name)
                              VALUES (?, ?);"""
            data_tuple = (self.max_id, self.lineEdit.text())
            self.cur.execute(sqlite_insert_with_param, data_tuple)
            self.connection.commit()
            self.formLayout.addRow(self.ingredientsLabelList[-1], self.delIngButtonList[-1])
        else:
            msg = QMessageBox(self)
            msg.setStyleSheet("background-color: rgb(255, 201, 60);")
            msg.setWindowTitle("Сообщение")
            msg.setText("Этот ингридент уже есть в списке")
            msg.exec_()

    def delIngredient(self):
        index = self.delIngButtonList.index(self.sender())
        if self.id_list[index] <= 24:
            msg = QMessageBox(self)
            msg.setStyleSheet("background-color: rgb(255, 201, 60);")
            msg.setWindowTitle("Сообщение")
            msg.setText("Нельзя удалить встроенный ингридиент!")
            msg.exec_()
        else:
            name = self.ingredientsLabelList[index].text()
            id = self.id_list[index]
            self.delIngButtonList[index].deleteLater()
            del self.delIngButtonList[index]
            self.ingredientsLabelList[index].deleteLater()
            del self.ingredientsLabelList[index]
            self.all_ingredients.remove(name)
            self.all_ingredients_id.remove(id)
            del self.id_list[index]
            sqlite_param = """DELETE from ingredients
                            where id = ?;"""
            data_tuple = (id,)
            self.cur.execute(sqlite_param, data_tuple)
            self.connection.commit()
            self.max_id = max(self.all_ingredients_id)


    def backToMain(self):
        self.cur.close()
        self.menu = main.Menu()
        self.menu.show()
        self.hide()
