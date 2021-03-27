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

    def wait(self):
        while not self.__pipe.poll(3):
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

                if option == 4:
                    self.__pipe.send({
                        'cmd': "info",
                        'src': "GUI",
                        'dst': 'kernel',
                        'msg': "sysinfo"
                    })

                    self.wait()

                    information = self.__pipe.recv()
                    _, option = interface.decide_option(option, 0, information['msg'])

                elif option == 2:
                    self.__pipe.send({
                        'cmd': 'info',
                        "src": "GUI",
                        "dst": "GestorArc",
                        "msg": "read"
                    })

                    self.wait()

                    information = self.__pipe.recv()
                    interface.decide_option(option, 0, information)

                elif option == 3:
                    _, option = interface.decide_option(option, 0)
                    self.__pipe.send({
                        'cmd': "info",
                        'src': "GUI",
                        "dst": "GestorArc",
                        "msg": f"folder:0:{_}"
                    })
                else:
                    interface.decide_option(option, 0)
            else:
                option = interface.input()
                if option == 1:
                    _, option = interface.decide_option(option, 1)
                    self.__pipe.send({
                        "cmd": "info",
                        "src": "GUI",
                        "dst": "applications",
                        "msg": f"launch:{_}"
                    })
                    option = 0
                else:
                    interface.decide_option(option, 1)

            print()
            time.sleep(2)
