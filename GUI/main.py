import time
import json
import threading

from multiprocessing.dummy.connection import Connection
from GUI.interface import Interface


class GUIMain:
    __pipe: Connection = None
    __thread = None

    def __init__(self, pipe):
        self.__pipe = pipe

    def listen_messages(self):
        while True:
            if not self.__pipe.poll(3):
                time.sleep(0.2)
                continue

    def start(self):
        self.__thread = threading.Thread(name="GUI/Messages", target=self.listen_messages)
        self.__thread.start()

        interface = Interface()
        option = 0
        
        time.sleep(2)
        while True:
            if option != 1:
                interface.main()
                option = interface.input()
                interface.decide_option(option, 0)
            else:
                option = interface.input()
                interface.decide_option(option, 1)




