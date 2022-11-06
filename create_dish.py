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
        self.all_con_id = []
        for ingr in self.cur.execute("""SELECT name FROM ingredients""").fetchall():
            self.all_ingredients.append(ingr[0])
        for dish_i in self.cur.execute("""SELECT id FROM dishes""").fetchall():
            self.all_dishes_id.append(dish_i[0])
        for con_i in self.cur.execute("""SELECT id FROM conections""").fetchall():
            self.all_con_id.append(con_i[0])
        self.ingredientsLabelList = []
        self.delIngButtonList = []
        self.massIngList = []
        self.idIngList = []
        self.allDishBut = []
        self.maxId = max(self.all_dishes_id)
        self.maxConId = max(self.all_con_id)
        self.noGirdLoad = True
        self.noDishGirdLoad = True
        self.ok.clicked.connect(self.appendIngredient)
        self.back.clicked.connect(self.backToMain)
        self.create.clicked.connect(self.createNewDish)
        self.ingName.addItems(self.all_ingredients)
        self.loadDishes()


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
        if self.nameDish.text().lower() not in [i[0].lower() for i in self.cur.execute("""SELECT name FROM dishes""").fetchall()]:
            if self.massDish.text().isdigit() and not self.massDish.text() == "":
                self.maxId = max(self.all_dishes_id) + 1
                self.all_dishes_id.append(self.maxId)
                print(self.maxId, "maxId")
                param = """INSERT INTO dishes
                                      (id, name, mass)
                                      VALUES (?, ?, ?);"""
                data = (self.maxId, self.nameDish.text(), int(self.massDish.text()))
                self.cur.execute(param, data)
                self.connection.commit()
                for ing_id in self.idIngList:
                    self.maxConId = max(self.all_con_id) + 1
                    self.all_con_id.append(self.maxConId)
                    index = self.idIngList.index(ing_id)

                    param = """INSERT INTO conections
                                      (id, ingridient_id, dish_id, mass)
                                      VALUES (?, ?, ?, ?);"""
                    data = (self.maxConId, ing_id, self.maxId, self.massIngList[index])
                    self.cur.execute(param, data)
                self.connection.commit()
                self.loadDishes()
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
            msg.setText('Такое блюдо уже есть!')
            msg.exec_()





    def loadDishes(self):
        if self.noDishGirdLoad:
            self.formLayout2 = QFormLayout()
            self.groupBox2 = QGroupBox()
            self.formLayout2.setContentsMargins(10, 10, 10, 10)
            self.groupBox2.setLayout(self.formLayout2)
            self.dishScroll.setWidget(self.groupBox2)
            self.dishScroll.setWidgetResizable(True)
            self.noDishGirdLoad = False
        self.dishes_id_in_rows = []

        for but in self.allDishBut:
            but.deleteLater()
        self.allDishBut = []
        for d_id in self.all_dishes_id:
            name = self.cur.execute("""SELECT name FROM dishes
                        WHERE id = ?""", (d_id,)).fetchall()[0][0]
            but = QPushButton(name)
            but.setStyleSheet("background-color: rgb(255, 111, 60);")
            self.dishes_id_in_rows.append(d_id)
            but.clicked.connect(self.delDish)
            self.allDishBut.append(but)
            self.formLayout2.addRow(self.allDishBut[-1])


    def delDish(self):
        index = self.allDishBut.index(self.sender())
        if self.dishes_id_in_rows[index] <= 10:
            msg = QMessageBox(self)
            msg.setStyleSheet("background-color: rgb(255, 201, 60);")
            msg.setWindowTitle("Сообщение")
            msg.setText("Нельзя удалить встроенное блюдо!")
            msg.exec_()
        else:
            id = self.dishes_id_in_rows[index]
            self.allDishBut[index].deleteLater()
            del self.allDishBut[index]
            del self.dishes_id_in_rows[index]
            self.all_dishes_id.remove(id)
            sqlite_param = """DELETE from dishes
                            where id = ?;"""
            data_tuple = (id,)
            self.cur.execute(sqlite_param, data_tuple)
            self.connection.commit()
            for con_id in self.cur.execute("""SELECT id FROM conections
                    WHERE dish_id = ?""", (id,)).fetchall():
                self.all_con_id.remove(con_id[0])
            sqlite_param = """DELETE from conections
                            where dish_id = ?;"""
            data_tuple = (id,)
            self.cur.execute(sqlite_param, data_tuple)
            self.connection.commit()
            self.loadDishes()


    def backToMain(self):
        self.menu = main.Menu()
        self.menu.show()
        self.hide()
