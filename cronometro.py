import threading
from time import sleep
from PyQt4.QtCore import *
from activities import Activity


class MiThread(threading.Thread):
    def __init__(self, widget, time_wait):
        threading.Thread.__init__(self)
        self.__widget = widget
        self.__widget.show()
        self.__time_wait = time_wait

    def run(self):
        for i in range(self.__time_wait):
            self.__widget.setText(str(self.__time_wait - i))
            sleep(1)
