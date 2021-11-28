import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from ui1 import Ui_MainWindow
from ui2 import Ui_MainWindow2


class Example(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

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
        self.setWindowTitle('Кофе')

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


class MyWidget(QMainWindow, Ui_MainWindow2):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.pushButton.clicked.connect(self.update_result)
        self.tableWidget.itemChanged.connect(self.item_changed)
        self.pushButton_2.clicked.connect(self.save_results)
        self.modified = {}
        self.titles = None
        self.setWindowTitle('Кофе')

    def update_result(self):
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM coffee WHERE id=?",
                             (item_id := self.spinBox.text(),)).fetchall()
        self.tableWidget.setRowCount(len(result))
        if not result:
            self.statusBar().showMessage('Ничего не нашлось')
            return
        else:
            self.statusBar().showMessage(f"Нашлась запись с id = {item_id}")
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}

    def item_changed(self, item):
        # Если значение в ячейке было изменено,
        # то в словарь записывается пара: название поля, новое значение
        self.modified[self.titles[item.column()]] = item.text()

    def save_results(self):
        if self.modified:
            cur = self.con.cursor()
            que = "UPDATE coffee SET\n"
            que += ", ".join([f"{key}='{self.modified.get(key)}'"
                              for key in self.modified.keys()])
            que += "WHERE id = ?"
            print(que)
            cur.execute(que, (self.spinBox.text(),))
            self.con.commit()
            self.modified.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    ex1 = MyWidget()
    ex1.show()
    sys.exit(app.exec())
