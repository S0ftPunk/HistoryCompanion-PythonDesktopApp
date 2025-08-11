import sys
import sqlite3
import pyperclip

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton,QLabel,QTextEdit,QListWidget,QListWidgetItem,QScrollBar
from PyQt5.QtCore import QSize,Qt,pyqtSignal,QEvent
from PyQt5.QtGui import QIcon,QPixmap


class Searcher: #Backend программы

    def min_max_date(self,file): #Возвращает минимально и максимально возможные даты
        db = sqlite3.connect("events_data.db")
        sql = db.cursor()
        dat = sql.execute(f'SELECT date FROM {file}').fetchall()
        event = sql.execute(f'SELECT event FROM {file}').fetchall()
        if file != "Asia":
            min_date = int(*dat[0])
        else:
            min_date = int(dat[0][0][0])
        max_date = int(*dat[-1])
        return f"Введите дату от {min_date} до {max_date}"

    def search(self,file,date): #Возвращает список с событиями, привязвнными к дате
        db = sqlite3.connect("events_data.db")
        sql = db.cursor()
        dat = sql.execute(f'SELECT date FROM {file}').fetchall()
        event = sql.execute(f'SELECT event FROM {file}').fetchall()
        if file != "Asia":
            min_date = int(*dat[0])
        else:
            min_date = int(dat[0][0][0])
        max_date = int(*dat[-1])
        event_list = []
        if date < min_date or date > max_date:
            print(f"Введите дату от {min_date} до {max_date}")
        else:
            for i in range(len(dat)):
                if str(date) in list(str(*dat[i]).split()):
                    event_list.append(*event[i])
        return event_list

    def add_to_notepad(self,lis,index): #Добавляет значение в таблицу блокнота
        db = sqlite3.connect("notepad.db")
        sql = db.cursor()
        sql.execute("""CREATE TABLE IF NOT EXISTS dates(
                        event TEXT,
                        id INTEGER         
        )""")
        db.commit()
        events = sql.execute('SELECT event FROM dates').fetchall()
        if len(events) == 0:
            idd = 0
        else:
            idd = int(*sql.execute('SELECT id FROM dates').fetchall()[-1])
        event_list = []
        for i in events:
            event_list.append(*i)
        if not(lis[index] in event_list):
            idd += 1
            sql.execute('INSERT INTO dates VALUES(?,?)',(lis[index],(idd)))
            db.commit()
        for i in sql.execute('SELECT event FROM dates').fetchall():
            print(*i)
            pass


class SearchScene(QWidget,Searcher): #Основная сцена приложения/поисковая сцена.Класс принимает название выбранной области(региона поиска)
    def __init__(self,country):
        super(SearchScene,self).__init__()
        self.setWindowTitle('HistoryCompanion')
        self.setWindowIcon(QIcon("pics\icon.png"))
        self.setMinimumSize(1130, 635)
        self.setMaximumSize(1130, 635)
        QMainWindow.setStyleSheet(self, """background-color:rgb(245,245,245)""")

        self.country = country

        pixmap = QPixmap("pics\logo.png")#лого
        logo = QLabel(self)
        logo.move(10, 20)
        logo.resize(85, 340)
        logo.setScaledContents(True)
        logo.setPixmap(pixmap)
        logo.setStyleSheet("""color:rgba(220,0,0,0)""")
        logo.show()

        f_scene = QPushButton(self)#Кнопка перехода на первую сцену
        f_scene.move(10,20)
        f_scene.resize(85,340)
        f_scene.setFlat(True)
        f_scene.setStyleSheet("""QPushButton:pressed
                                {
                                background-color:rgba(230,230,230,30);
                                border:0;
                                }""")
        f_scene.clicked.connect(self.show_first_scene)
        f_scene.show()

        self.textedit = QTextEdit(self)#Поисковая строка
        self.textedit.resize(560,50)
        self.textedit.move(285,100)
        self.textedit.setStyleSheet("""background-color:white;
                                       border:1px solid rgb(53,53,53);
                                       font-family:Calibri;
                                       font-weight:lighter;
                                       font-size:24pt;
                                       color:rgb(20,20,20);""")
        self.textedit.setText(self.min_max_date(country))
        self.textedit.show()
        self.textedit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textedit.viewport().installEventFilter(self)

        note_button = QPushButton(self)#Кнопка перехода в блокнот
        note_button.setIcon(QIcon("pics\qnote.png"))
        note_button.move(1030,30)
        note_button.resize(50,50)
        note_button.setIconSize(QSize(45,45))
        note_button.setFlat(True)
        note_button.setStyleSheet("""QPushButton:pressed
                                {
                                background-color:rgb(230,230,230);
                                border:0;
                                }""")
        note_button.clicked.connect(self.show_noteScene)
        note_button.show()

        searchB = QPushButton(self)#Кнопка поиска
        searchB.setIcon(QIcon("pics\search_button.png"))
        searchB.move(796,101)
        searchB.resize(48,48)
        searchB.setIconSize(QSize(48,48))
        searchB.setFlat(True)
        searchB.setStyleSheet("""QPushButton:pressed
                                {
                                background-color:rgb(245,245,245);
                                border:0;
                                }""")
        searchB.clicked.connect(self.show_events)
        searchB.show()

        self.listwidget = QListWidget(self)#ListWidget отвечает за отображение результатов
        self.listwidget.move(120,179)
        self.listwidget.resize(1010,456)
        self.listwidget.setStyleSheet("""QListWidget
                                        {
                                        font-family:Calibri;
                                        font-weight:lighter;
                                        font-size:20px;
                                        color:rgb(20,20,20);
                                        border: none;
                                        }
                                        QListWidget::item {
                                        border-bottom: 1px solid rgb(180,180,180);
                                        text-align: center;
                                        margin-right:20px;                              
                                        }
                                        """)
        scrol_bar = QScrollBar()
        scrol_bar.setStyleSheet("""
                                 QScrollBar:vertical {
                                            width:25px;                                            
                                        }
                                        QScrollBar::handle {
                                            background: rgb(180,180,180);                                                                                    
                                        }
                                        QScrollBar::handle:vertical {
                                            height: 25px;                                            
                                        }""")
        self.listwidget.setVerticalScrollBar(scrol_bar)
        self.listwidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listwidget.setWordWrap(True)
        self.listwidget.show()
        self.save_list = []

    def show_events(self):#Выводит в ListWidget результаты
        if self.textedit.toPlainText().isdigit():
            date = int(self.textedit.toPlainText())
            events_list  = self.search(self.country,date)
            self.listwidget.clear()
            for i in range(len(events_list)):
                item = QListWidgetItem()
                item.setText(events_list[i])
                add_button = QPushButton(self) #Кнопка добавления результата в блокнот
                add_button.resize(50, 50)
                add_button.setStyleSheet(
                                        """
                                        QPushButton:pressed
                                        {
                                        background-color:rgba(200,255,200,50);
                                        border:0;
                                        }""")
                add_button.setFlat(True)
                add_button.setObjectName(str(i))
                add_button.clicked.connect(lambda: self.add_to_notepad(events_list, int(self.sender().objectName())))
                self.listwidget.addItem(item)
                self.listwidget.setItemWidget(item, add_button)
        else:
            self.textedit.setText(self.min_max_date(self.country))

    def show_noteScene(self): #Переключение на сцену блокнота, передает значение country, чтобы вернуть его на сцену поиска
        self.s = NoteScene(self.country)
        self.s.show()
        SearchScene.close(self)

    def show_first_scene(self): #Показ первой сцены/сцены выбора территории
        self.f = FirstScene()
        self.f.show()
        SearchScene.close(self)

    def eventFilter(self, obj, event): #Очищает поисковую строку по нажатию мыши
        if obj is self.textedit.viewport() and event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                self.textedit.clear()
        return super().eventFilter(obj, event)


class NoteScene(QWidget): # Сцена блокнота
    def __init__(self,country):
        super(NoteScene, self).__init__()
        self.setWindowTitle('HistoryCompanion')
        self.setWindowIcon(QIcon("pics\icon.png"))
        self.setMinimumSize(1130, 635)
        self.setMaximumSize(1130, 635)
        QMainWindow.setStyleSheet(self, """background-color:rgb(245,245,245)""")

        self.country = country

        pixmap = QPixmap("pics\logo.png") # Лого
        logo = QLabel(self)
        logo.move(10, 20)
        logo.resize(85, 340)
        logo.setScaledContents(True)
        logo.setPixmap(pixmap)
        logo.show()

        f_scene = QPushButton(self) # Кнопка перехода на первую сцену
        f_scene.move(10, 20)
        f_scene.resize(85, 340)
        f_scene.setFlat(True)
        f_scene.setStyleSheet("""QPushButton:pressed
                                        {
                                        background-color:rgba(230,230,230,30);
                                        border:0;
                                        }""")
        f_scene.clicked.connect(self.show_first_scene)
        f_scene.show()

        search_scene_B = QPushButton(self) # Кнопка перехода на поисковую сцену
        search_scene_B.resize(48, 48)
        search_scene_B.move(1030, 30)
        search_scene_B.setIcon(QIcon("pics\search_button.png"))
        search_scene_B.setIconSize(QSize(48, 48))
        search_scene_B.setFlat(True)
        search_scene_B.setStyleSheet("""QPushButton:pressed
                                {
                                background-color:rgb(230,230,230);
                                border:0;
                                }""")
        search_scene_B.clicked.connect(lambda :FirstScene.show_search_scene(self,self.country))
        search_scene_B.show()

        del_all = QPushButton(self)# Кнопка очищения блокнота
        del_all.resize(42,56)
        del_all.move(10,570)
        del_all.setIcon(QIcon("pics\del_b.png"))
        del_all.setIconSize(QSize(42,56))
        del_all.setFlat(True)
        del_all.setStyleSheet("""QPushButton:pressed
                                {
                                background-color:rgb(230,230,230);
                                border:0;
                                }""")
        del_all.clicked.connect(self.dellAll)
        del_all.show()

        copy_all = QPushButton(self)# Кнопка, копирующая все значения в блокноте
        copy_all.resize(48, 48)
        copy_all.move(541, 30)
        copy_all.setIcon(QIcon("pics\copy_b.png"))
        copy_all.setIconSize(QSize(48, 48))
        copy_all.setFlat(True)
        copy_all.setStyleSheet("""QPushButton:pressed
                                      {
                                      background-color:rgb(230,230,230);
                                      border:0;
                                      }""")
        copy_all.clicked.connect(self.copyAll)
        copy_all.show()

        self.show_events()
    def show_first_scene(self):# Переход на первую сцену
        self.f = FirstScene()
        self.f.show()
        SearchScene.close(self)
    def show_events(self): # Выводит результаты в ListWidget
        self.listwidget = QListWidget(self)
        self.listwidget.move(95, 90)
        self.listwidget.resize(1074, 590)
        self.listwidget.setStyleSheet("""QListWidget
                                                        {
                                                        font-family:Calibri;
                                                        font-weight:lighter;
                                                        font-size:20px;
                                                        color:rgb(20,20,20);
                                                        border: none;
                                                        margin:none;                                               
                                                        }
                                                        QListWidget::item {
                                                        border-bottom: 1px solid rgb(180,180,180);
                                                        text-align: center;
                                                        margin-right:20px;

                                                        }
                                                        """)
        scrol_bar = QScrollBar()
        scrol_bar.setStyleSheet("""
                                                 QScrollBar:vertical {
                                                            width:25px;
                                                        }
                                                        QScrollBar::handle {
                                                            background: rgb(170,170,170);
                                                            border-radius: 35px;
                                                        }
                                                        QScrollBar::handle:vertical {
                                                            height: 25px;
                                                        }""")
        self.listwidget.setVerticalScrollBar(scrol_bar)
        self.listwidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listwidget.setWordWrap(True)
        self.listwidget.show()

        self.db = sqlite3.connect("notepad.db")
        self.sql = self.db.cursor()
        self.save_event_list = self.sql.execute("SELECT event FROM dates").fetchall()
        for i in range(len(self.save_event_list)):
            item = QListWidgetItem()
            copy_button = QPushButton(self)
            copy_button.resize(50, 50)
            copy_button.setStyleSheet(
                """
                QPushButton:pressed
                {
                background-color:rgba(200,200,255,50);
                border:0;
                }""")
            copy_button.setFlat(True)
            copy_button.setObjectName(str(i))
            item.setText(*self.save_event_list[i])
            self.listwidget.addItem(item)
            self.listwidget.setItemWidget(item,copy_button)
    def dellAll(self): # Очищает sql данные и listWidget
        self.sql.execute("""DELETE FROM dates""")
        self.db.commit()
        self.listwidget.clear()
    def copyAll(self): #Копирует все результаты
        str = []
        s = ""
        for i in range(len(list(self.save_event_list))):
            str.append(*self.save_event_list[i])
        for i in str:
            s += i
        pyperclip.copy(s)


class FirstScene(QMainWindow): #Сцена выбора территории/первая сцена
    def __init__(self):
        super(FirstScene, self).__init__()
        self.setWindowTitle('HistoryCompanion')
        self.setWindowIcon(QIcon("pics\icon.png"))
        self.setMinimumSize(1130,635)
        QMainWindow.setStyleSheet(self,"""background-color:rgb(245,245,245)""")

        pixmap = QPixmap("pics\logo.png") #Лого
        logo = QLabel(self)
        logo.move(10,20)
        logo.resize(85,340)
        logo.setScaledContents(True)
        logo.setPixmap(pixmap)
        logo.show()

        label = QLabel(self) #Надпись верхняя
        label.move(140,40)
        label.resize(890,60)
        label.setText("Выберите территорию, история которой вам интересна")
        label.setStyleSheet("""font-family:Calibri;
                               font-weight:lighter;
                               font-size:24pt;
                               color:rgb(20,20,20);                        
                               """)
        label.setAlignment(Qt.AlignCenter)


        stylesheet = """QPushButton
                                {
                                border: 1px solid gray;
                                color:rgb(20,20,20);
                                font-family:Calibri;
                                font-weight:lighter;
                                font-size:24px;
                                }
                                QPushButton:pressed
                                {
                                background-color:rgb(239,239,239);
                                border:1px solid gray;
                                }"""

        # Далее идет загрузка картинок контуров стран
        self.p_r = QPixmap("pics\qrussia_gray.png")
        self.russia_k = QLabel(self)
        self.russia_k.move(574,141)
        self.russia_k.resize(464,164)
        self.russia_k.setPixmap(self.p_r)
        self.russia_k.setStyleSheet("background-color:rgba(0,0,0,0);")
        self.russia_k.show()

        self.p_a = QPixmap("pics\qasia_gray.png")
        self.asia_k = QLabel(self)
        self.asia_k.move(584, 250)
        self.asia_k.resize(328, 222)
        self.asia_k.setPixmap(self.p_a)
        self.asia_k.setStyleSheet("background-color:rgba(0,0,0,0);")
        self.asia_k.show()

        self.p_e = QPixmap("pics\europ_gray.png")
        self.europ_k = QLabel(self)
        self.europ_k.move(419, 176)
        self.europ_k.resize(198, 171)
        self.europ_k.setPixmap(self.p_e)
        self.europ_k.setStyleSheet("background-color:rgba(0,0,0,0);")
        self.europ_k.show()

        self.p_usa = QPixmap("pics\qamerika_gray.png")
        self.usa_k = QLabel(self)
        self.usa_k.move(150, 220)
        self.usa_k.resize(218, 150)
        self.usa_k.setPixmap(self.p_usa)
        self.usa_k.setStyleSheet("background-color:rgba(0,0,0,0);")
        self.usa_k.show()

        #Далее идут кнопки выбора стран/осуществляют переход на сцену поиска, передают в нее значение country
        europB = Button(self)
        europB.setText("Европа")
        europB.move(332,500)
        europB.resize(180,60)
        europB.setStyleSheet(stylesheet)
        europB.clicked.connect(lambda: self.show_search_scene("Europ"))
        europB.setMouseTracking(True)
        europB.changeColor.connect(lambda : self.colorChange("europ"))
        europB.stayColor.connect(lambda : self.colorStay("europ"))
        europB.show()

        ruB = Button(self)
        ruB.setText("Россия")
        ruB.move(564, 500)
        ruB.resize(180,60)
        ruB.setStyleSheet(stylesheet)
        ruB.clicked.connect(lambda: self.show_search_scene("russia"))
        ruB.setMouseTracking(True)
        ruB.changeColor.connect(lambda : self.colorChange("russia"))
        ruB.stayColor.connect(lambda : self.colorStay("russia"))
        ruB.show()

        usaB = Button(self)
        usaB.setText("США")
        usaB.move(100,500)
        usaB.resize(180, 60)
        usaB.setStyleSheet(stylesheet)
        usaB.clicked.connect(lambda: self.show_search_scene("USA"))
        usaB.setMouseTracking(True)
        usaB.changeColor.connect(lambda : self.colorChange("usa"))
        usaB.stayColor.connect(lambda : self.colorStay("usa"))
        usaB.show()

        asiaB = Button(self)
        asiaB.setText("Азия")
        asiaB.move(796, 500)
        asiaB.resize(180, 60)
        asiaB.setStyleSheet(stylesheet)
        asiaB.clicked.connect(lambda:self.show_search_scene("Asia"))
        asiaB.setMouseTracking(True)
        asiaB.changeColor.connect(lambda: self.colorChange("asia"))
        asiaB.stayColor.connect(lambda: self.colorStay("asia"))
        asiaB.show()

    def show_search_scene(self,country):  #Переход на сцену поиска
        self.s = SearchScene(country)
        self.s.show()
        FirstScene.close(self)
    def colorChange(self,country):  #Меняет цвет контура страны на красный по наведению на соотв. кнопку
        if country == "russia":
            self.p_r = QPixmap("pics\qrussia_red.png")
            self.russia_k.setPixmap(self.p_r)
        if country == "europ":
            self.p_e = QPixmap("pics\europ_red.png")
            self.europ_k.setPixmap(self.p_e)
        if country == "asia":
            self.p_a = QPixmap("pics\qasia_red.png")
            self.asia_k.setPixmap(self.p_a)
        if country == "usa":
            self.p_usa = QPixmap("pics\qamerika_red.png")
            self.usa_k.setPixmap(self.p_usa)

    def colorStay(self, country):  #Меняет цвет контура страны на серый по выведению курсора с соотв. кнопки
        if country == "russia":
            self.p_r = QPixmap("pics\qrussia_gray.png")
            self.russia_k.setPixmap(self.p_r)
        if country == "europ":
            self.p_e = QPixmap("pics\europ_gray.png")
            self.europ_k.setPixmap(self.p_e)
        if country == "asia":
            self.p_a = QPixmap("pics\qasia_gray.png")
            self.asia_k.setPixmap(self.p_a)
        if country == "usa":
            self.p_usa = QPixmap("pics\qamerika_gray.png")
            self.usa_k.setPixmap(self.p_usa)


class Button(QPushButton): #Отвечает за отслеживания курсора. Нужно для изменения цвета контуров стран
    changeColor = pyqtSignal()
    stayColor = pyqtSignal()

    def mouseMoveEvent(self, event):
        self.changeColor.emit()

    def leaveEvent(self, event):
        self.stayColor.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = FirstScene()
    w.show()
    sys.exit(app.exec_())
