# coding=utf-8
__author__ = 'adrian'
from data.questions.level1 import level_1
from data.info.info import random_color
from data.questions.level2 import level_2
from data.questions.level3 import level_3
from data.questions.level4 import level_4
from data.questions.english import english, spanish
import shelve
from helper import capitalize_finalize
from random import randint
from app import config

random_list = list()


class Question():
    def __init__(self, dict_=None):
        if not dict_:
            dict_ = {}
        self.__color = random_color()
        self.__dict_ = dict_
        self.__random_list = []

    @property
    def color(self):
        return self.__color

    def dict_keys(self):
        return self.__dict_.keys()

    def dict_values(self, key):
        return self.__dict_[key]

    def random_item(self, file_key):
        """
        Usamos un dict para serializar las preguntas previmente mostradas, en toda la historia, no importa que se haya
        cerrado el juego, hasta que no se cumpla el ciclo de mostrar todas las preguntas no se empeaara un nuevo ciclo.
        Tambien se resetea la lista de random que se almacena en memoria, por si el jugador tuvo una larga jornada de juego,
        y se muestran todas las preguntas en el mismo partido.
        :param file_key: el nivel de la preguunta para almacenarlo como key del dict a serializar
        :return: una pregunta random que no se haya seleccionado previamente
        """
        shelf = shelve.open(config["data_file"])
        try:
            historical_quest = shelf[file_key]
            if len(historical_quest) >= len(self.dict_keys()):
                historical_quest = []
        except KeyError:
            historical_quest = []
            shelf[file_key] = historical_quest
        if len(self.__random_list) >= len(self.dict_keys()):
            self.__random_list = []
        while True:
            random_quest = self.dict_keys()[randint(0, len(self.dict_keys()) - 1)]
            if random_quest not in self.__random_list and \
                            random_quest not in historical_quest:
                self.__random_list.append(random_quest)
                historical_quest.append(random_quest)
                shelf[file_key] = historical_quest
                return random_quest


class Level1(Question):
    def __init__(self):
        Question.__init__(self, level_1)


class Level4(Question):
    def __init__(self):
        Question.__init__(self, level_4)


class Level3(Question):
    def __init__(self):
        Question.__init__(self, level_3)


class Level2(Question):
    def __init__(self):
        Question.__init__(self, level_2)


class English(Question):
    def __init__(self):
        dict_ = {}
        length = len(english)
        # recorremos las palabras que seram quest
        for i in range(length):
            # escoger el sentido de la pregunta spn - eng o eng -spn
            random_number = randint(0, 999)
            if random_number < 500:
                list_anw = spanish
                list_quest = english
            else:
                list_anw = english
                list_quest = spanish
            answers = []
            pos_tmp = []
            # escoger 3 palabras al azar que no sean la actual
            while True:
                pos = randint(0, length - 1)
                if pos != i and pos not in pos_tmp:
                    answers.append(capitalize_finalize(list_anw[pos]))
                    pos_tmp.append(pos)
                    if len(answers) == 3:
                        break
            # ubicamos la palabra actual como otra respuesta y como real answ, ademas del "" por el btn profundiza
            answers.extend([capitalize_finalize(list_anw[i]), capitalize_finalize(list_anw[i]), ""])
            # creamos la key del dict con la quest actual
            dict_[capitalize_finalize(list_quest[i])] = answers
        # llamamos al constructor de Question
        Question.__init__(self, dict_)


English()

