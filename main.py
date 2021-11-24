import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableView


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.initUI()

    def initUI(self):
        self.bd()
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('coffee.sqlite')
        db.open()

        view = self.tableView
        model = QSqlTableModel(self, db)
        model.setTable('coffee')
        model.select()

        view.setModel(model)
        view.move(10, 10)
        view.resize(617, 315)

        self.setGeometry(300, 100, 650, 450)
        self.setWindowTitle('Пример работы с QtSql')

    def bd(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS coffee(
               ID INT PRIMARY KEY,
               name TEXT,
               degree_of_roasting TEXT,
               consistency TEXT,
               description TEXT,
               price INT,
               volume INT
               );
            """)

        zn1 = [(1, 'Бразильский', 'средняя', 'молотый', 'вкусный', 150, 500), (2, 'Колумбийский', 'слабая', 'в зёрнах',
                                                                               'не такой вкусный', 120, 600),
               (3, 'Гавайский', 'сильная', 'в зёрнах', 'невкусный', 110, 550), (4, 'Индийский', 'средняя', 'молотый',
                                                                                'очень вкусный', 300, 450)]
        zp1 = """INSERT OR IGNORE INTO coffee(ID, name, degree_of_roasting, consistency, description, price, volume) \
        VALUES(?, ?, ?, ?, ?, ?, ?)"""
        cur.executemany(zp1, zn1)
        con.commit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
