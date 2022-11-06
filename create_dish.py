from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QListView, QComboBox, QPushButton, QFormLayout, QGroupBox, QMessageBox
import sqlite3
import main


class CreateDish(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('cteate_dish.ui', self)
        self.connection = sqlite3.connect("Meals.db")
        self.cur = self.connection.cursor()
        self.all_ingredients = []
        self.all_dishes_id = []
        for ingr in self.cur.execute("""SELECT name FROM ingredients""").fetchall():
            self.all_ingredients.append(ingr[0])
        for dish_i in self.cur.execute("""SELECT id FROM dishes""").fetchall():
            self.all_dishes_id.append(dish_i[0])
        self.ingredientsLabelList = []
        self.delIngButtonList = []
        self.massIngList = []
        self.idIngList = []
        self.maxId = max(self.all_dishes_id)
        self.noGirdLoad = True
        self.ok.clicked.connect(self.appendIngredient)
        self.back.clicked.connect(self.backToMain)
        self.create.clicked.connect(self.createNewDish)
        self.ingName.addItems(self.all_ingredients)


    def appendIngredient(self):
        if self.ingName.currentText().lower() in [i.lower() for i in self.all_ingredients]:
            if self.ingMass.text().isdigit() and not self.ingMass.text() == "":
                if self.noGirdLoad:
                    self.formLayout = QFormLayout()
                    self.groupBox = QGroupBox()
                    self.formLayout.setContentsMargins(10, 10, 10, 10)
                    self.groupBox.setLayout(self.formLayout)
                    self.ingScroll.setWidget(self.groupBox)
                    self.ingScroll.setWidgetResizable(True)
                    self.noGirdLoad = False
                if self.ingName.currentText().lower() not in [self.cur.execute("""SELECT name FROM ingredients
                            WHERE id = ?""", (i,)).fetchall()[0][0].lower() for i in self.idIngList]:
                    self.ingredientsLabelList.append(QLabel(self.ingName.currentText() + " " + self.ingMass.text() + "г"))
                    self.idIngList.append(self.cur.execute("""SELECT id FROM ingredients
                            WHERE name = ?""", (self.ingName.currentText().lower().capitalize(),)).fetchall()[0][0])
                    print(self.idIngList)
                    self.massIngList.append(self.ingMass.text())
                    but = QPushButton("Удалить")
                    but.setStyleSheet("background-color: rgb(255, 111, 60);")
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
                msg.setText('Масса должна быть числом!')
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
        del self.idIngList[index]
        del self.massIngList[index]

    def createNewDish(self):
        if self.massDish.text().isdigit() and not self.massDish.text() == "":
            self.maxId = max(self.all_dishes_id) + 1
            self.all_dishes_id.append(self.maxId)
            print(self.maxId)
            param = """INSERT INTO dishes
                                  (id, name, mass)
                                  VALUES (?, ?, ?);"""
            data = (self.maxId, self.nameDish.text(), int(self.massDish.text()))
            self.cur.execute(param, data)
            self.connection.commit()


        else:
            msg = QMessageBox(self)
            msg.setStyleSheet("background-color: rgb(255, 201, 60);")
            msg.setWindowTitle("Сообщение")
            msg.setText('Масса должна быть числом!')
            msg.exec_()

    def backToMain(self):
        self.menu = main.Menu()
        self.menu.show()
        self.hide()
