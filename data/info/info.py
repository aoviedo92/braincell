# coding=utf-8
from random import randint

__author__ = 'adrian'
# import history, universe

# history1 = history.history_level_1
# universe1 = universe.universe_level_1

# info_list = [history1,
#              universe1]
info_list = []

def get_info(question):
    for dict_ in info_list:
        try:
            info = dict_[question].split('\n')
            # print("info", info)
            return info
        except KeyError:
            continue

__types = {
    "Selecciona": "#5d4799",
    "Cierto Falso": "#e82350",
    u"Inglés": "#e11785",
    # "Ciencia": "#279ed8",
    # "Planeta Tierra": "#987d2e",
    # "Vida": "#f7b518",
    # "Deporte": "#23aa4b",
    # "Medicina": "#0873b9",
    # "Tecnologia": "#1eb7c9",
    # "Arte": "#DAA520"
    }

def get_types():
    return __types

def random_color():
    colors = __types.values()
    return colors[randint(0, len(colors) - 1)]