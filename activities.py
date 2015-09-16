# coding=utf-8
__author__ = 'adrian'
from random import randint
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from helper import *
from ui.imagebutton import ImageButton
from app import config
import shelve


class ActionBar(QFrame):
    def __init__(self, parent=None):
        super(ActionBar, self).__init__(parent)
        self.marker = QLabel("0")
        self.coins = ImageButton(":/coins", size=(35, 45))
        self.btn_back = ImageButton(":/back", size=(35, 45))
        self.btn_probability_quest = ImageButton(":/rayo", size=(35, 45), tooltip="Compra las posibilidades de acertar")
        self.btn_hide_quest = ImageButton(":/ver", size=(35, 45), tooltip="Escoge de entre dos")
        self.btn_1 = ImageButton(":/bombilla", size=(35, 45), tooltip="??")
        self.btn_random_quest = ImageButton(":/random", size=(35, 45), tooltip="Cambia esta pregunta")
        self.btn_probability_quest.setEnabled(False)
        self.btn_hide_quest.setEnabled(False)
        self.btn_random_quest.setEnabled(False)
        layout = QHBoxLayout()
        layout.addWidget(self.coins)
        layout.addWidget(self.marker)
        layout.addWidget(self.btn_back)
        layout.addStretch(1)
        layout.addWidget(self.btn_probability_quest)
        layout.addWidget(self.btn_hide_quest)
        # layout.addWidget(self.btn_1)
        layout.addWidget(self.btn_random_quest)
        self.setLayout(layout)
        self.move(0, 0)
        self.setFixedSize(config["width"], 50)
        self.btn_random_quest.setObjectName("btn_random")
        self.marker.setMinimumWidth(400)
        self.marker.setObjectName("marker")
        self.setObjectName("action_bar")
        self.setStyleSheet("background-color: coral;")
        self.marker.setStyleSheet("font: 18px; color: #ffbb33; font-weight: bold")
        self.marker.setMinimumWidth(40)
        self.show_coins()
        self.hide()

    def show_coins(self):
        self.coins.show()
        self.marker.show()
        self.btn_back.hide()

    def show_back(self):
        self.btn_back.show()
        self.coins.hide()
        self.marker.hide()

    def animation_geometry(self, widget, init=(200, 300, 0, 0), end=(0, 50, 400, 550), finish=None, duration=250):
        init_rect = QRect(init[0], init[1], init[2], init[3])
        end_rect = QRect(end[0], end[1], end[2], end[3])
        self.animation = QPropertyAnimation(widget, "geometry")
        self.animation.setStartValue(init_rect)
        self.animation.setEndValue(end_rect)
        self.animation.setDuration(duration)
        self.animation.start()
        if finish:
            self.connect(self.animation, SIGNAL('finished()'), finish)

    def move_coins_from_top(self):
        y1 = self.marker.y() - 80
        y2 = y1 + 40
        self.animation_geometry(self.marker,
                                init=(self.marker.x(), y1, self.marker.width(), self.marker.height()),
                                end=(self.marker.x(), y2, self.marker.width(), self.marker.height()))

    def move_coins_bottom(self, text):
        self.marker.setText(text)
        self.animation_geometry(self.marker,
                                init=(self.marker.x(), self.marker.y(), self.marker.width(), self.marker.height()),
                                end=(self.marker.x(), self.marker.y() + 40, self.marker.width(), self.marker.height()),
                                finish=self.move_coins_from_top)


class Activity(QFrame):
    def __init__(self, parent=None):
        super(Activity, self).__init__(parent)
        self.move(0, 50)
        self.resize(config["width"], config["height"] - 100)
        self.hide()
        self.setStyleSheet(self.qss())

    @staticmethod
    def qss():
        return """
                Activity{
                    background-color: #fff;
                }
            """

    def animation_slide(self, widget, init=0, end=400, finish=None, duration=250):
        height = widget.height()
        self.animation = QPropertyAnimation(widget, "size")
        self.animation.setStartValue(QSize(init, height))
        self.animation.setEndValue(QSize(end, height))
        self.animation.setDuration(duration)
        self.animation.start()
        if finish:
            self.connect(self.animation, SIGNAL('finished()'), finish)

    def static_animation(self, widget, duration=250, finish=None):
        height = widget.height()
        init = widget.width()
        end = widget.width()
        self.animation = QPropertyAnimation(widget, "size")
        self.animation.setStartValue(QSize(init, height))
        self.animation.setEndValue(QSize(end, height))
        self.animation.setDuration(duration)
        self.animation.start()
        if finish:
            self.connect(self.animation, SIGNAL('finished()'), finish)

    def animation_geometry(self, widget, init=(200, 300, 0, 0), end=(0, 50, 400, 550), finish=None, duration=250):
        init_rect = QRect(init[0], init[1], init[2], init[3])
        end_rect = QRect(end[0], end[1], end[2], end[3])
        self.animation = QPropertyAnimation(widget, "geometry")
        self.animation.setStartValue(init_rect)
        self.animation.setEndValue(end_rect)
        self.animation.setDuration(duration)
        self.animation.start()
        if finish:
            self.connect(self.animation, SIGNAL('finished()'), finish)


class InitActivity(Activity):
    def __init__(self, parent=None):
        super(InitActivity, self).__init__(parent)
        self.btn = QPushButton("")
        self.tiles = []
        modes = ["Selecciona", "Cierto Falso", u"Inglés"]
        colors = ["#5d4799", "#e82350", "#e11785", "#279ed8", "#987d2e", "#f7b518", "#23aa4b", "#0873b9", "#1eb7c9",
                  "#DAA520", "#8A2BE2", "#DC143C", "#7B68EE", "#3CB371", "#BA55D3", "#32CD32", "#800000", "#FF4500",
                  "#FF8C00", "#FFD700"]
        color_random = [colors[randint(0, len(colors) - 1)] for i in range(len(modes))]
        for mode, color in zip(modes, color_random):
            tile = QPushButton(mode)
            tile.setCursor(QCursor(Qt.PointingHandCursor))
            tile.setStyleSheet("background-color: " + color)
            self.tiles.append(tile)
        positions = [(i, j) for i in range(1, len(self.tiles)) for j in range(2)]
        lbl = QPushButton("Seleccione un modo de juego")
        lbl.setStyleSheet("height: 50px; color: coral; font: 24px \"Calibri\"")
        grid = QGridLayout()
        grid.addWidget(lbl, 0, 0, 1, 0)
        for pos, tile in zip(positions, self.tiles):
            grid.addWidget(tile, *pos)
        self.setLayout(grid)
        self.setStyleSheet(self.qss_())

    @staticmethod
    def qss_():
        return """
            QPushButton{
                height: 200px;
                border: 0;
                border-radius: 50px;
                color: #fff;
                font: 18px \"Calibri\"
            }
        """


class ActivityQuestion(Activity):
    def __init__(self, question, answers, real_answer, color, parent=None):
        super(ActivityQuestion, self).__init__(parent)
        self.question = QPushButton()
        self.question.setEnabled(False)
        self.set_text_and_minimum_height(self.question, question)
        self.real_answer = real_answer
        self.color = color
        self.answers = list()
        layout = QVBoxLayout()
        layout.addStretch(1)
        layout.addWidget(self.question)
        layout.addStretch(1)
        answers = self.ubi_btn_randomize(answers)
        for ans in answers:
            btn = QPushButton()
            self.set_text_and_minimum_height(btn, ans)
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            self.answers.append(btn)
            layout.addWidget(btn)
        layout.addStretch(1)
        self.question.setObjectName("question")
        self.setLayout(layout)
        self.setStyleSheet(self.qss_())

    def answers_text(self):
        return [unicode(btn.text()).replace("\n", " ") for btn in self.answers]

    @staticmethod
    def ubi_btn_randomize(list_):
        random_list_0_3 = []
        while len(random_list_0_3) <= 3:
            r = randint(0, 3)
            if r not in random_list_0_3:
                random_list_0_3.append(r)
        unsorted_result_list = [0] * 4
        for e, i in zip(list_, random_list_0_3):
            unsorted_result_list[i] = e
        return unsorted_result_list

    @staticmethod
    def set_text_and_minimum_height(widget, text):
        text = new_line(text)
        lines_jump = len(text.split("\n"))
        line_height = 40
        if lines_jump <= 1:
            height = line_height
        else:
            height = lines_jump * line_height - lines_jump * line_height / 4
        widget.setText(text)
        widget.setMinimumHeight(height)

    def show(self):
        self.animation_geometry(self)
        self.setVisible(True)

        # def hide(self):
        # self.animation_slide(self, init=400, end=0)
        # self.setVisible(False)

    def qss_(self):
        return """
            #question{
                font: 25px \"Calibri\";
                background-color: #fff;
                border: 0;
                color: %s;
            }

            QPushButton:hover{
                color: #FF4500;
                /*border-bottom: 1px solid %s;*/
                background-color: #FAFAFA;
                font-weight: bold;
            }
            QPushButton{
                font: 20px \"Calibri\";
                color: %s;
                background-color: #fff;
                border-radius: 4px;
                height: 50px;
                border: 0px solid %s;
            }
            /*ActivityQuestion{
                background-color: #fff;
            }*/
            """ % (self.color, self.color, self.color, self.color)


class ActivityProfundiza(Activity):
    def __init__(self, question, parent=None):
        super(ActivityProfundiza, self).__init__(parent)
        self.browser = QTextBrowser()
        info = question.split('\n')
        title = info.pop(0)
        title = u'<h1 style="color: coral; text-align: center;">%s<h1>' % title
        self.browser.append(title)
        for parrafo in info:
            self.browser.append(u'<p style="font-size: 12px; text-align: justify;">%s</p>' % parrafo)
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        self.setLayout(layout)
        self.setStyleSheet(self.qss_())

    @staticmethod
    def qss_():
        return """
                QTextBrowser{
                    border: 0;
                }
                QScrollBar {
                    border: 0px solid grey;
                    width: 7px;
                }
                QScrollBar::handle {
                    background: antiquewhite;
                    border-radius: 3px;
                    /*border: 1px solid coral;*/
                }
                QScrollBar::handle:hover{
                    background: coral;
                }
            """


class SlideFrame(Activity):
    def __init__(self, parent=None):
        super(SlideFrame, self).__init__(parent)
        self.height_ = 50
        self.setStyleSheet("background-color: coral;")
        self.time_to_be = 2000

    def set_height(self, height):
        self.height_ = height

    def set_time_to_be(self, time):
        self.time_to_be = time

    def show(self):
        self.setVisible(True)
        self.animation_geometry(self,
                                init=(0, 50, config["width"], 0),
                                end=(0, 50, config["width"], self.height_),
                                finish=self.to_be)

    def to_be(self):
        self.static_animation(self, finish=self.hide_, duration=self.time_to_be)

    def hide_(self):
        self.animation_geometry(self,
                                init=(0, 50, 400, self.height_),
                                end=(0, 50, 400, 0))


class Notification(SlideFrame):
    def __init__(self, text, parent=None):
        super(Notification, self).__init__(parent)
        self.text = QPushButton(unicode(text))
        self.text.setStyleSheet("color: #ffbb33; font: 20px; border: 0;")
        self.text.setMinimumWidth(config["width"])
        self.set_height(50)
        layout = QHBoxLayout()
        layout.addWidget(self.text)
        self.setLayout(layout)
        self.show()


class FramePayProbability(Activity):
    def __init__(self, coins, parent=None):
        super(FramePayProbability, self).__init__(parent)
        self.resize(config["width"], 50)
        self.total_coins = coins
        self.trust = str()
        twenty_percent = self.total_coins * 20 / 100
        self.spin = QSpinBox()
        self.spin.setMaximum(self.total_coins)
        self.spin.setValue(twenty_percent)
        self.btn_show_probability = QPushButton(
            u"Calcula la probabilidad,\n mientras más pagues más probabilidades tendrás de acertar")
        self.btn_show_probability.setMinimumWidth(310)
        self.btn_show_probability.setCursor(QCursor(Qt.PointingHandCursor))
        layout = QHBoxLayout()
        layout.addWidget(ImageButton(":/coins", size=(20, 20)))
        layout.addWidget(self.spin)
        layout.addWidget(self.btn_show_probability)
        self.setLayout(layout)
        self.connect(self.spin, SIGNAL('valueChanged(int)'), self.calculate_percent)
        # self.connect(self.spin, SIGNAL('returnPressed()'), self.calculate_percent)
        self.setStyleSheet(self.qss_())
        self.show()

    @staticmethod
    def qss_():
        return """
        FramePayProbability{
            background-color: coral;
        }
        QPushButton{
            border: 0;
            color: #fff;
        }
        QPushButton:hover{
            border: 0;
            /*background-color: #FA7F4E;*/
            /*border-radius: 4px;*/
            color: brown;
            /*border-bottom: 1px solid brown;*/
        }
        QSpinBox{
            border: 1px solid brown;
            background-color: #fff;
            padding: 4px;
        }
        """

    def calculate_percent(self):
        trust_ = self.spin.value() * 100 / self.total_coins
        if trust_ >= 80:  # P ALTA
            self.trust = "ALTA"
        elif 60 <= trust_ < 80:  # P BUENA
            self.trust = "BUENA"
        elif 40 <= trust_ < 60:  # P MEDIA
            self.trust = "MEDIA"
        elif 20 <= trust_ < 40:  # P BAJA
            self.trust = "BAJA"
        elif 0 <= trust_ < 20:  # P MALA
            self.trust = "MALA"
        self.btn_show_probability.setText("PROBABILIDAD %s" % self.trust)


class CharmProbability(SlideFrame):
    def __init__(self, pb, parent=None):
        super(CharmProbability, self).__init__(parent)
        self.set_time_to_be(5000)
        self.set_height(200)
        layout = QHBoxLayout()
        for p in pb:
            lbl = QPushButton(str(p))
            lbl.setFixedSize(p + 50, p + 50)
            lbl.setStyleSheet("background-color: #9ACD32; color: #708090; font-weight: bold;border-radius: %spx" % str(
                randint(5, 25)))
            layout.addWidget(lbl)
        self.setLayout(layout)
        self.setStyleSheet("background-color: #f4f4f4")
        self.show()


class SummaryActivity(Activity):
    def __init__(self, parent=None):
        super(SummaryActivity, self).__init__(parent)
        self.btn_play_again = QPushButton("Jugar de nuevo")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.btn_play_again.setMinimumHeight(200)
        self.btn_play_again.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_play_again.setObjectName("btn_again")
        self.btn_play_again.setStyleSheet(self.btn_again_qss_())

    @staticmethod
    def btn_again_qss_():
        return """
        #btn_again{
            font: 24px \"Calibri\";
            border: 0; background-color: #9ACD32; color: #708090; border-radius: 60px;
        }
        #btn_again:hover{
            background-color: #ADFF2F;
        }
        """


class YouWinActivity(SummaryActivity):
    def __init__(self, parent=None):
        super(YouWinActivity, self).__init__(parent)
        self.file = "data.dat"
        self.data = []
        self.widget = []
        self.deserealize()
        self.line_your_name = QLineEdit()
        self.layout_records = QVBoxLayout()
        self.layout.addStretch(1)
        self.layout.addWidget(self.line_your_name)
        self.layout.addLayout(self.layout_records)
        self.layout.addStretch(1)
        self.layout.addWidget(self.btn_play_again)
        self.populate()
        self.setStyleSheet(self.qss_())

    def populate(self):
        self.remove()
        for row in self.data:
            lbl = QPushButton("%s - %d" % (row[0], row[1]))
            self.layout_records.addWidget(lbl)
            self.widget.append(lbl)

    def remove(self):
        while self.widget:
            lbl = self.widget.pop()
            lbl.hide()
            self.layout_records.removeWidget(lbl)

    def serialize(self, player_name, player_coins):
        if player_name.strip():
            self.data.append((player_name, player_coins))
        # data = file(self.file, "w", 2)
        self.data = sorted_couple(self.data)[:5]
        shelf = shelve.open(config["data_file"])
        shelf["records"] = self.data
        shelf.close()
        # pickle.dump(self.data, data, 2)
        # data.close()
        self.populate()

    def deserealize(self):
        shelf = shelve.open(config["data_file"])
        try:
            self.data = shelf["records"]
        except KeyError:
            print(1)
            shelf["records"] = []

    @staticmethod
    def qss_():
        return """
        QLineEdit{
            font: 14px \"Calibri\";
            height: 35px;
            border: 1px solid #9ACD32;
            color: #9ACD32;
            padding-left: 4px;
            font-weight: bold;
        }
        QPushButton{
            border: 0;
            border-bottom: 1px solid #9ACD32;
            height: 40px;
            color: #9ACD32;
            font-weight: bold;
        }
        """


class GameOverActivity(SummaryActivity):
    def __init__(self, parent=None):
        super(GameOverActivity, self).__init__(parent)
        self.lbl_game_over = QPushButton()
        self.layout.addWidget(self.lbl_game_over)
        self.layout.addWidget(self.btn_play_again)

        self.lbl_game_over.setStyleSheet("""
        border: 0;
        font: 24px \"Calibri\";
        color: #9ACD32;
        """)
