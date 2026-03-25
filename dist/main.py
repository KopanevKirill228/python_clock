import sys
import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import QTimer, Qt
from проект6 import Ui_MainWindow
from проект7 import Ui_Dialog1
from проект9 import Ui_Dialog
from PyQt5 import QtCore, QtMultimedia
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
# Наследуемся от виджета из PyQt5.QtWidgets и от класса с интерфейсом


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.step = 0
        # Вызываем метод для загрузки интерфейса из класса Ui_MainWindow,
        # остальное без изменений
        self.picture()
        self.setupUi(self)
        self.fname = 'standart_melody.mp3'
        self.install_melody.clicked.connect(self.install)
        self.info_autor.clicked.connect(self.open_third_form)
        self.Clock()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.Clock)
        self.timer.start(1000)
        self.timer1 = QTimer(self)
        self.timer2 = QTimer(self)
        self.timer1.timeout.connect(self.update_func)
        self.timer2.timeout.connect(self.bydilnic)
        self.timer2.start(1000)
        self.begin.clicked.connect(self.cekyndomer)
        self.reset.clicked.connect(self.reset1)
        self.install_clock.clicked.connect(self.install_clock_sql)
        # sql таблица
        self.con = sqlite3.connect('SQL_BD.db')
        self.cur = self.con.cursor()
        self.cur1 = self.con.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS alarmclock (
        id     INTEGER PRIMARY KEY AUTOINCREMENT
                   UNIQUE
                   NOT NULL,
        title  STRING  NOT NULL,
        hour   INTEGER NOT NULL,
        minute INTEGER NOT NULL,
        melody STRING  NOT NULL
        );'''
        )
        self.con.commit()

    def Clock(self):
        # реальное время в столицах
        self.calendar.clicked.connect(self.open_second_form)
        current_datetime = datetime.datetime.now()
        hour = current_datetime.hour
        minute = current_datetime.minute
        delta_time1 = datetime.timedelta(hours=-1)
        delta_time2 = datetime.timedelta(hours=6)
        delta_time3 = datetime.timedelta(hours=-1)
        current_datetime1 = current_datetime + delta_time1
        hour1 = current_datetime1.hour
        minute1 = current_datetime1.minute
        current_datetime2 = current_datetime + delta_time2
        hour2 = current_datetime2.hour
        minute2 = current_datetime2.minute
        current_datetime3 = current_datetime + delta_time3
        hour3 = current_datetime3.hour
        minute3 = current_datetime3.minute
        if len(str(minute)) == 1:
            minute = '0' + str(minute)
        if len(str(minute1)) == 1:
            minute1 = '0' + str(minute1)
        if len(str(minute2)) == 1:
            minute2 = '0' + str(minute2)
        if len(str(minute3)) == 1:
            minute3 = '0' + str(minute3)
        time = str(hour) + ':' + str(minute)
        time1 = str(hour1) + ':' + str(minute1)
        time2 = str(hour2) + ':' + str(minute2)
        time3 = str(hour3) + ':' + str(minute3)
        self.time_Moscow1.display(time)
        self.time_Berlin1.display(time1)
        self.time_Tokio1.display(time2)
        self.time_Kiev1.display(time3)

    def cekyndomer(self):
        if not self.timer1.isActive():
            self.begin.setText('Stop')
            self.timer1.start(10)
        else:
            self.begin.setText('Start')
            self.timer1.stop()

    def bydilnic(self):
        # поиск будильника
        time_now = datetime.datetime.now()
        hour_now = str(time_now.hour)
        minute_now = str(time_now.minute)
        result = self.cur.execute("""SELECT melody FROM alarmclock
                    WHERE
                        (hour = ?) AND (minute = ?)
                        """, (hour_now, minute_now)).fetchall()
        result1 = self.cur.execute("""DELETE from alarmclock
                    WHERE
                        (hour = ?) AND (minute = ?)
                        """, (hour_now, minute_now))
        for elem in result:
            self.load_mp3(elem[0])
            self.player.play()
        self.stop.clicked.connect(self.stop1)
        self.delete_last.clicked.connect(self.delete_alarm_clock)
        self.con.commit()

    def update_func(self):
        # секундомер
        self.step += 0.01
        self.seconds.setText(str(round(self.step, 3)))

    def reset1(self):
        if self.timer1.isActive():
            self.timer1.stop()
        self.seconds.setText(str(0))
        self.step = 0

    def load_mp3(self, filename):
        # воспроизведение музыки
        media = QtCore.QUrl.fromLocalFile(filename)
        content = QtMultimedia.QMediaContent(media)
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setMedia(content)

    def install(self):
        self.fname = QFileDialog.getOpenFileName(
            self, 'Выбрать мелодию', '',
            'Мелодия (*.mp3);;Все файлы (*)')[0]

    def install_clock_sql(self):
        # запись будильника в sql таблицу
        hour, minute = self.time_clock.text().split(':')
        self.cur.execute('''INSERT INTO alarmclock(title, hour, minute, melody) VALUES(?, ?, ?, ?)''',
                         (self.name.text(), hour, minute, self.fname))
        self.con.commit()

    def open_second_form(self):
        # вторая форма для календаря
        self.second_form = SecondForm(self, "Данные для второй формы")
        self.second_form.show()

    def stop1(self):
        # остановка музыки из будильника
        self.player.stop()

    def delete_alarm_clock(self):
        self.cur.execute('''DELETE from alarmclock
            where id = (SELECT MAX(id) FROM alarmclock)''')
        self.con.commit()

    def picture(self):
        ## Изображение
        self.pixmap = QPixmap('alarm.jpg')
        # Если картинки нет, то QPixmap будет пустым,
        # а исключения не будет
        self.image = QLabel(self)
        self.image.move(370, 250)
        self.image.resize(250, 250)
        # Отображаем содержимое QPixmap в объекте QLabel
        self.image.setPixmap(self.pixmap)

    def open_third_form(self):
        # вторая форма для календаря
        self.third_form = ThirdForm(self, "Данные для второй формы")
        self.third_form.show()


class SecondForm(QWidget, Ui_Dialog1):
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)


class ThirdForm(QWidget, Ui_Dialog):
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)
        self.Picture_autor()
        self.sql_table()
        self.replace_label()

    def sql_table(self):
        self.con = sqlite3.connect('SQL_BD.db')
        self.cur1 = self.con.cursor()
        self.cur1.execute('''CREATE TABLE IF NOT EXISTS autor (
        family  STRING NOT NULL,
        imya    STRING NOT NULL,
        city    STRING NOT NULL,
        country STRING NOT NULL,
        number  STRING NOT NULL,
        Otch    STRING NOT NULL
        );
        '''
        )
        self.cur1.execute('''INSERT INTO autor(family, imya, city, country, number, Otch) VALUES(?, ?, ?, ?, ?, ?)''',
                         ('Копанев', 'Кирилл', 'Киров', 'Россия', '89127271558', 'Артемович'))
        self.con.commit()

    def Picture_autor(self):
        self.pixmap = QPixmap('author.jpg')
        # Если картинки нет, то QPixmap будет пустым,
        # а исключения не будет
        self.image = QLabel(self)
        self.image.move(255, -20)
        # Отображаем содержимое QPixmap в объекте QLabel
        self.image.setPixmap(self.pixmap)

    def replace_label(self):
        result = self.cur1.execute("""SELECT imya, Otch, family, city, country, number FROM autor
                    WHERE family = ?
                        """, ('Копанев',))
        for i in result:
            self.label_2.setText(i[0])
            self.label_6.setText(i[1])
            self.label_4.setText(i[2])
            self.label_10.setText(i[3])
            self.label_8.setText(i[4])
            self.label_12.setText(str(i[5]))

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyWidget()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
