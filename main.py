import io
import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


DB_NAME = "data/coffee.sqlite"

template = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>800</width>
    <height>600</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Обзор сортов кофе</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <layout class="QVBoxLayout" name="verticalLayout">
    <item>
     <layout class="QHBoxLayout" name="horizontalLayout">
      <item>
       <widget class="QPushButton" name="addButton">
        <property name="text">
         <string>Добавить</string>
        </property>
       </widget>
      </item>
      <item>
       <spacer name="horizontalSpacer">
        <property name="orientation">
         <enum>Qt::Horizontal</enum>
        </property>
        <property name="sizeHint" stdset="0">
         <size>
          <width>40</width>
          <height>20</height>
         </size>
        </property>
       </spacer>
      </item>
     </layout>
    </item>
    <item>
     <widget class="QTableWidget" name="tableWidget"/>
    </item>
   </layout>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>800</width>
     <height>26</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
"""

add_template = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Form</class>
 <widget class="QWidget" name="Form">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>400</width>
    <height>396</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Добавить сорт кофе</string>
  </property>
  <widget class="QPlainTextEdit" name="sort">
   <property name="geometry">
    <rect>
     <x>110</x>
     <y>10</y>
     <width>281</width>
     <height>31</height>
    </rect>
   </property>
   <property name="focusPolicy">
    <enum>Qt::StrongFocus</enum>
   </property>
  </widget>
  <widget class="QLabel" name="label">
   <property name="geometry">
    <rect>
     <x>9</x>
     <y>10</y>
     <width>81</width>
     <height>31</height>
    </rect>
   </property>
   <property name="text">
    <string>Название сорта</string>
   </property>
  </widget>
  <widget class="QPlainTextEdit" name="taste">
   <property name="geometry">
    <rect>
     <x>110</x>
     <y>160</y>
     <width>281</width>
     <height>61</height>
    </rect>
   </property>
   <property name="focusPolicy">
    <enum>Qt::StrongFocus</enum>
   </property>
  </widget>
  <widget class="QLabel" name="label_2">
   <property name="geometry">
    <rect>
     <x>9</x>
     <y>160</y>
     <width>81</width>
     <height>31</height>
    </rect>
   </property>
   <property name="text">
    <string>Описаное</string>
   </property>
  </widget>
  <widget class="QLabel" name="label_3">
   <property name="geometry">
    <rect>
     <x>10</x>
     <y>110</y>
     <width>81</width>
     <height>31</height>
    </rect>
   </property>
   <property name="text">
    <string>Молотый  в зернах</string>
   </property>
  </widget>
  <widget class="QComboBox" name="grains">
   <property name="geometry">
    <rect>
     <x>110</x>
     <y>110</y>
     <width>281</width>
     <height>26</height>
    </rect>
   </property>
  </widget>
  <widget class="QPlainTextEdit" name="price">
   <property name="geometry">
    <rect>
     <x>110</x>
     <y>240</y>
     <width>281</width>
     <height>31</height>
    </rect>
   </property>
  </widget>
  <widget class="QLabel" name="label_4">
   <property name="geometry">
    <rect>
     <x>10</x>
     <y>240</y>
     <width>81</width>
     <height>31</height>
    </rect>
   </property>
   <property name="text">
    <string>Стоиммость</string>
   </property>
  </widget>
  <widget class="QPushButton" name="pushButton">
   <property name="geometry">
    <rect>
     <x>240</x>
     <y>340</y>
     <width>141</width>
     <height>41</height>
    </rect>
   </property>
   <property name="text">
    <string>Добавить</string>
   </property>
  </widget>
  <widget class="QLabel" name="label_5">
   <property name="geometry">
    <rect>
     <x>9</x>
     <y>60</y>
     <width>81</width>
     <height>16</height>
    </rect>
   </property>
   <property name="text">
    <string>Степень обжарка</string>
   </property>
  </widget>
  <widget class="QComboBox" name="roast">
   <property name="geometry">
    <rect>
     <x>110</x>
     <y>60</y>
     <width>281</width>
     <height>26</height>
    </rect>
   </property>
  </widget>
  <widget class="QLabel" name="label_6">
   <property name="geometry">
    <rect>
     <x>9</x>
     <y>300</y>
     <width>81</width>
     <height>31</height>
    </rect>
   </property>
   <property name="text">
    <string>Развес</string>
   </property>
  </widget>
  <widget class="QPlainTextEdit" name="volume">
   <property name="geometry">
    <rect>
     <x>110</x>
     <y>290</y>
     <width>281</width>
     <height>31</height>
    </rect>
   </property>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
"""


class AddWidget(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        ui_file = io.StringIO(add_template)
        uic.loadUi(ui_file, self)
        self.con = sqlite3.connect(DB_NAME)
        self.params_roast = {}
        self.select_roast()
        self.params_grain = {}
        self.select_grain()
        self.pushButton.clicked.connect(self.add_elem)
        self.__is_adding_successful = False

    def select_roast(self):
        req = "SELECT * from roasts"
        cur = self.con.cursor()
        for value, key in cur.execute(req).fetchall():
            self.params_roast[key] = value
        self.roast.addItems(list(self.params_roast.keys()))

    def select_grain(self):
        req = "SELECT * from grain"
        cur = self.con.cursor()
        for value, key in cur.execute(req).fetchall():
            self.params_grain[key] = value
        self.grains.addItems(list(self.params_grain.keys()))

    def add_elem(self):
        cur = self.con.cursor()
        try:
            id = cur.execute("SELECT max(id) FROM coffe").fetchone()[0] + 1
            sort = self.sort.toPlainText()
            roast = self.params_roast.get(self.roast.currentText())
            grains = self.params_grain.get(self.grains.currentText())
            taste = self.taste.toPlainText()
            price = float(self.price.toPlainText())
            volume = int(self.volume.toPlainText())

            # отловление ошибок
            if len(sort) == 0:
                raise ValueError('sort lenght == 0')
            if price < 0:
                raise ValueError('price <= 0')

            new_data = (id, sort, roast, grains, taste, price, volume)
            cur.execute("INSERT INTO coffe VALUES (?,?,?,?,?,?,?)", new_data)
            self.__is_adding_successful = True
        except ValueError as ve:
            self.__is_adding_successful = False
            self.statusBar().showMessage("Неверно заполнена форма")
        else:
            self.con.commit()
            self.parent().update_result()
            self.close()

    def get_adding_verdict(self):
        return self.__is_adding_successful


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_file = io.StringIO(template)
        uic.loadUi(ui_file, self)
        self.con = sqlite3.connect(DB_NAME)
        self.update_result()
        self.addButton.clicked.connect(self.adding)
        self.add_form = None

    def update_result(self):
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        que = "SELECT c.id, c.sort, r.roast, g.grains, c.taste, c.price, c.volume " \
              "FROM coffe as c JOIN roasts as r ON c.roast = r.id JOIN grain as g " \
              "ON c.grains = g.id ORDER BY c.id DESC"
        result = cur.execute(que).fetchall()

        # Заполнили размеры таблицы
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setHorizontalHeaderLabels(
            ['ИД', 'Сорт кофе', 'Степень обжарки', 'Молотый .. в зернах',
             'Описание вкуса', 'Стоимость', 'Развес'])

        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def adding(self):
        self.add_form = AddWidget(self)
        self.add_form.show()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyWidget()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
