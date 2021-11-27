import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class Coffee(QDialog):  # Диалог создания нового элемента в словаре тривиалочек
    def __init__(self, con, table):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.okbutton.clicked.connect(self.save)
        self.con = con
        self.table = table

    def save(self):
        gr = self.group.currentText()
        return [self.table, [self.name.text(), self.roast.text(), str(gr), self.desc.toPlainText(),
                             str(self.price.value()), str(self.volume.value())]]


class NewCoffee(Coffee):
    def __init__(self, con, table):
        super().__init__(con, table)
        self.setWindowTitle("Новое название")

    def save(self):
        data = super().save()
        x = "INSERT INTO " + data[0] + "(sortname, roast, ground, desc, price, volume) VALUES('" + \
            "', '".join(data[1]) + "')"
        self.con.execute(x)
        self.con.commit()
        self.close()


class EditCoffee(Coffee):
    def __init__(self, con, table, row):
        super().__init__(con, table)
        self.setWindowTitle("Редактировать")
        self.row = self.con.cursor().execute("SELECT * FROM coffees").fetchall()[row]
        self.rown = row + 1
        self.name.setText(self.row[1])
        self.roast.setText(self.row[2])
        gr = self.row[3]
        self.group.setCurrentIndex(['Молотый', 'В зёрнах'].index(gr))
        self.desc.setPlainText(self.row[4])
        self.price.setValue(self.row[5])
        self.volume.setValue(self.row[6])

    def save(self):
        data = super().save()
        print(data)
        x = "UPDATE " + data[0] + " SET sortname = '" + data[1][0] + \
            "', roast = '" + data[1][1] + "', ground = '" + data[1][2] + "', desc = '" + data[1][3] + "', price = " + \
            data[1][4] + ", volume = " + data[1][5]
        x += " WHERE ID = " + str(self.rown)
        x += " WHERE ID = " + str(self.rown)
        print(x)
        self.con.cursor().execute(x)
        self.con.commit()
        self.close()


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.con = sqlite3.connect("coffee.sqlite")
        cur = self.con.cursor()
        result = cur.execute('SELECT * from coffees').fetchall()
        print(result)
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Название", "Степень обжарки", "Молотый/в зернах",
                                                    "Описание", "Цена", "Объём"])
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.doubleClicked.connect(self.editcoffee)
        self.pushButton.clicked.connect(self.newcoffee)

    def update_table(self):
        res = self.con.execute("SELECT * FROM coffees")
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        # Заполняем таблицу элементами
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

    def newcoffee(self):
        new = NewCoffee(self.con, 'coffees')
        new.exec()
        self.update_table()

    def editcoffee(self, mi):
        edit = EditCoffee(self.con, 'coffees', mi.row())
        edit.exec()
        self.update_table()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
