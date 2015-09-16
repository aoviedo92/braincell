# coding=utf-8
__author__ = 'adrian'
import ctypes
import sys
from activities import *
from PyQt4.QtCore import *
from questions import *
from datetime import datetime
from pistas import probabilidades
from app import config
import resources

APP_ID = 'dev$oviedo.DoYouKnowMe-PyQt4.v1.0'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)


class Form(Activity):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.MODE_CHOOSE = False
        self.MODE_TRUE_FALSE = False
        self.MODE_ENGLISH = False
        self.coins = 0
        self.level = 1
        self.questions = 0
        self.random = False
        self.trick = False
        self.game_over = False
        self.trick_state = [0, 0, 0]
        self.notify_once = [1, 2, 3, 4]
        self.current_activity = object()
        self.time_wait = 30
        self.start_time = None
        self.profundiza = unicode()
        self.obj_level_1 = Level1()
        self.obj_level_2 = Level2()
        self.obj_level_3 = Level3()
        self.obj_level_4 = Level4()
        self.english = English()

        self.action_bar = ActionBar(self)
        self.activity_you_win = YouWinActivity(self)
        self.activity_game_over = GameOverActivity(self)

        self.btn_profundiza = QPushButton("Profundiza", self)

        self.activity_question = QFrame
        self.set_ui()
        self.connects()
        self.show_init_activity()

    def init_vars(self):
        self.MODE_CHOOSE = False
        self.MODE_TRUE_FALSE = False
        self.MODE_ENGLISH = False
        self.coins = 0
        self.level = 1
        self.questions = 0
        self.random = False
        self.trick = False
        self.game_over = False
        self.trick_state = [0, 0, 0]
        self.notify_once = [1, 2, 3, 4]

    def connects(self):
        self.connect(self.activity_game_over.btn_play_again, SIGNAL('released()'), self.play_again)
        self.connect(self.activity_you_win.btn_play_again, SIGNAL('released()'), self.you_win)
        self.connect(self.action_bar.btn_back, SIGNAL('released()'), self.show_question)
        self.connect(self.btn_profundiza, SIGNAL('released()'), self.show_profundiza)
        self.connect(self.action_bar.btn_random_quest, SIGNAL('released()'), self.random_pass_this)
        self.connect(self.action_bar.btn_hide_quest, SIGNAL('released()'), self.hide_two_question)
        self.connect(self.action_bar.btn_probability_quest, SIGNAL('released()'), self.show_probability_pay)

    def show_probability_pay(self):
        global pay
        pay = FramePayProbability(self.coins, self)
        self.connect(pay.btn_show_probability, SIGNAL('released()'), self.show_probability_charm)
        self.connect(pay.spin, SIGNAL('returnPressed()'), self.show_probability_charm)

    def show_probability_charm(self):
        self.trick = True
        self.trick_state[0] = True
        pay.hide()
        answers = [unicode(ans.text()) for ans in self.activity_question.answers]
        answers.append(self.activity_question.real_answer)
        self.coins -= pay.spin.value()
        self.animate_marker_coins()
        self.state_of_action_bar_buttons()
        pb = probabilidades.probability(answers, self.coins, pay.spin.value(), pay.trust)
        CharmProbability(pb, self)
        self.action_bar.btn_probability_quest.setEnabled(False)

    def random_pass_this(self):
        self.random = True
        self.trick = True
        self.trick_state[2] = True
        self.coins -= self.coins * 25 / 100
        self.animate_marker_coins()
        self.state_of_action_bar_buttons()
        self.action_bar.btn_random_quest.setEnabled(False)
        self.show_question()

    def hide_two_question(self):
        # buscar la pos de real_answ
        self.trick = True
        self.trick_state[1] = True
        pos_real_answ = 0
        for btn in self.activity_question.answers:
            if unicode(btn.text()).replace("\n", " ") == self.activity_question.real_answer:
                break
            pos_real_answ += 1
        # seleccionar dos numeros aleatorios que difieran entre si y de la real answ
        while True:
            pos1 = randint(0, 3)
            if pos1 != pos_real_answ:
                pos2 = randint(0, 3)
                if pos2 != pos1 and pos2 != pos_real_answ:
                    break
        # ocultar botones
        self.animation_slide(self.activity_question.answers[pos1],
                             init=config["width"], end=0,
                             finish=self.activity_question.answers[pos1].hide)
        self.activity_question.answers[pos2].hide()
        self.coins -= self.coins * 30 / 100
        self.animate_marker_coins()
        self.state_of_action_bar_buttons()
        self.action_bar.btn_hide_quest.setEnabled(False)

    def show_profundiza(self):
        self.action_bar.show_back()
        global activity_profundiza
        activity_profundiza = ActivityProfundiza(self.profundiza, self)
        self.change_activity(activity_profundiza)

    def state_of_action_bar_buttons(self):
        self.action_bar.btn_probability_quest.setEnabled(
            True if self.coins > 300 and not self.trick_state[0] else False)
        self.action_bar.btn_random_quest.setEnabled(True if self.coins > 100 and not self.trick_state[2] else False)
        self.action_bar.btn_hide_quest.setEnabled(True if self.coins > 200 and not self.trick_state[1] else False)

    def animate_btn_profundiza(self):
        if not self.MODE_ENGLISH:
            self.btn_profundiza.show()
        self.animation_geometry(self.btn_profundiza,
                                init=(config["width"] / 2, config["height"] - 50, 0, 50),
                                end=(0, config["height"] - 50, 400, 50),
                                finish=self.animate_show_next_question,
                                duration=1000)

    def animate_marker_coins(self):
        self.action_bar.move_coins_bottom(str(self.coins))

    def animate_show_next_question(self):
        if self.game_over:
            self.static_animation(self.activity_question,
                                  finish=self.show_activity_game_over,
                                  duration=3750)
        else:
            self.static_animation(self.activity_question,
                                  finish=self.show_question,
                                  duration=3750)

    def show_activity_game_over(self):
        if self.MODE_CHOOSE:
            text = "Te has quedado en\nla pregunta %d, en el nivel %d" % (self.questions, self.level)
        elif self.MODE_ENGLISH:
            text = u"Tu puntuacón es de %d monedas" % self.coins
        self.activity_game_over.lbl_game_over.setText(text)
        self.reset()
        self.change_activity(self.activity_game_over)

    def show_init_activity(self):
        global init_activity
        init_activity = InitActivity(self)
        self.current_activity = init_activity
        for tile in init_activity.tiles:
            tile.clicked.connect(self.clicked_tile)
        init_activity.show()

    def clicked_tile(self):
        sender = self.sender()
        btn_clicked = unicode(sender.text())
        if btn_clicked == "Selecciona":
            self.MODE_CHOOSE = True
        elif btn_clicked == "Cierto Falso":
            self.MODE_TRUE_FALSE = True
        elif btn_clicked == u"Inglés":
            self.MODE_ENGLISH = True
        self.show_question()

    def change_activity(self, go_activity, gone_activity=None):
        if not gone_activity:
            gone_activity = self.current_activity
        self.current_activity = go_activity
        self.animation_slide(gone_activity,
                             init=config["width"], end=0,
                             finish=go_activity.show,
                             duration=100)

    # def notification_start(self, text):
    # Notification(text, self)

    def choose(self):
        sender = self.sender()
        text = unicode(sender.text()).replace("\n", " ")
        if text == self.activity_question.real_answer:
            sender.setStyleSheet("background-color: #00FA9A; border: 0; border-radius:0")
            correct = sender
            # determinar el tiempo que se demoro en realizar la pregunta
            delta = datetime.now() - self.start_time
            if self.MODE_TRUE_FALSE or self.MODE_CHOOSE:
                v1 = (self.time_wait - delta.seconds) * self.level
                # si se demoro mas de lo estimado, solo establecer 50
                if v1 < 0:
                    v1 = 50
                else:
                    v1 += 50
                if not self.trick:
                    self.coins += v1
                    self.state_of_action_bar_buttons()
            elif self.MODE_ENGLISH:
                self.coins += 1
            self.animate_marker_coins()
        else:
            # si la respuesta n es correcta marcarla de rojo, y relucir la correcta en verde
            # mostrar pantalla del game over
            self.game_over = True
            sender.setStyleSheet("background-color: #DC143C; border: 0")
            for btn in self.activity_question.answers:
                if unicode(btn.text()).replace("\n", " ") == self.activity_question.real_answer:
                    correct = btn
                    btn.setStyleSheet("background-color: #00FA9A; border: 0; border-radius:0")
                    break
        # desabilitar todos los btn respuestas
        for btn in self.activity_question.answers:
            btn.setEnabled(False)
        self.trick = False
        self.animation_geometry(correct,
                                init=(correct.x(), correct.y(), correct.width(), correct.height()),
                                end=(0, correct.y(), correct.width() + 20, correct.height()),
                                finish=self.animate_btn_profundiza,
                                duration=250)

    def find_level_and_key_mode_choose(self):
        if not self.random:
            self.questions += 1
        if self.questions <= 4:
            self.level = 1
        if 4 < self.questions <= 8:
            self.level = 2
        if 8 < self.questions <= 12:
            self.level = 3
        if 12 < self.questions <= 16:
            self.level = 4
        if self.questions == 17:
            self.level = 5

        if self.level == 1:
            key = self.obj_level_1.random_item("level1")
            values = self.obj_level_1.dict_values(key)
            color = self.obj_level_1.color
        elif self.level == 2:
            key = self.obj_level_2.random_item("level2")
            values = self.obj_level_2.dict_values(key)
            color = self.obj_level_2.color
        elif self.level == 3:
            key = self.obj_level_3.random_item("level3")
            values = self.obj_level_3.dict_values(key)
            color = self.obj_level_3.color
        elif self.level == 4:
            key = self.obj_level_4.random_item("level3")
            values = self.obj_level_4.dict_values(key)
            color = self.obj_level_4.color
        elif self.level == 5:
            # mostrar activity resumen (aqui se muestra un resultado ganador) y se muestran las coins
            # la implementacion esta en set_question --- TypeError
            return
        self.random = False
        return key, values, color

    def set_question(self):
        print "set question"
        try:
            if self.MODE_CHOOSE:# or self.MODE_TRUE_FALSE:
                key, values, color = self.find_level_and_key_mode_choose()
            elif self.MODE_ENGLISH:
                key = self.english.random_item("english")
                values = self.english.dict_values(key)
                color = self.english.color
            self.activity_question = ActivityQuestion(key,
                                                      values[:-2],  # respuestas
                                                      values[-2],  # respuesta real
                                                      color, self)
            self.profundiza = values[-1]
            self.btn_profundiza.setStyleSheet("""border-radius: 25px;
                                                 border: 0px solid black;
                                                 color: #fff;
                                                 background-color: """ + color)
            for btn in self.activity_question.answers:
                btn.clicked.connect(self.choose)
        except TypeError:
            # este error se lanza cuando level == 5 no se establecen las vars key, values, color
            # self.activity_you_win.lbl_your_record.setText(str(self.coins))
            self.activity_you_win.line_your_name.setPlaceholderText(
                u"Tu puntuación es de %s, escribe tu nombre para almacenarla" % self.coins)
            self.change_activity(self.activity_you_win)
            self.disable_action_bar_btn()
            return "You_Win"

    def you_win(self):
        # serializar el nombre del jugador y las monedas obtenidas
        self.activity_you_win.serialize(unicode(self.activity_you_win.line_your_name.text()), self.coins)
        self.activity_you_win.line_your_name.clear()
        self.reset()
        self.play_again()

    def disable_action_bar_btn(self):
        self.action_bar.btn_random_quest.setEnabled(False)
        self.action_bar.btn_hide_quest.setEnabled(False)
        self.action_bar.btn_probability_quest.setEnabled(False)

    def play_again(self):
        self.activity_you_win.hide()
        self.activity_game_over.hide()
        self.show_init_activity()

    def reset(self):
        self.init_vars()
        self.animate_marker_coins()
        self.btn_profundiza.hide()
        self.disable_action_bar_btn()

    def show_question(self):
        self.action_bar.show()
        init_activity.hide()
        self.action_bar.show_coins()
        self.btn_profundiza.hide()
        self.start_time = datetime.now()
        if self.set_question() != "You_Win" and not self.game_over:
            self.change_activity(self.activity_question)
            if not self.MODE_ENGLISH: # no mostrar estas notificaciones cuando el mode sea ingles
                if self.notify_once[self.level - 1]:
                    Notification("nivel " + str(self.level), self)
                    self.notify_once[self.level - 1] = False
        if self.game_over:
            # si llegamos a aqui por mediacion del btn back de la action bar ocultamos el panel profundiza
            activity_profundiza.hide()
            self.reset()
            self.play_again()

    def set_ui(self):
        self.setWindowTitle(config["name"])
        self.setWindowIcon(QIcon(config["icon"]))
        self.move(config["width"], 0)
        self.setFixedSize(config["width"], config["height"])
        self.btn_profundiza.hide()
        self.btn_profundiza.move(config["width"] / 2, config["height"] - 25)


app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()