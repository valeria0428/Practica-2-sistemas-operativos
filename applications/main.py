import time
import json
import logging
import threading

from multiprocessing.dummy.connection import Connection


class ApplicationsMain:
    __pipe = None
    __apps = []

    def __init__(self, pipe: Connection):
        self.__pipe = pipe

    def start(self):
        self.listen_messages()

    def listen_messages(self):
        while True:
            if not self.__pipe.poll(3):
                time.sleep(0.2)
                continue

            message = self.__pipe.recv()

            message = message.split(':')

            if len(message) == 0 and message[0] == "halt":
                self.__pipe.send({
                    "cmd": "stop",
                    "src": "applications",
                    "dst": "kernel",
                    "msg": "Stopped by user"
                })
                self.halt_apps()
            else:
                if message[0] == "launch":
                    self.launch_app(message[1])
                if message[0] == "stop":
                    self.halt_apps(message[1])

    def halt_apps(self, app=None):
        if app:
            _app = next((__app for __app in self.__apps if __app['pid'] == app), None)
            if _app is None:
                logging.error("Thread not founded")

            _app['thread']._stop()
            _app['treaad'].join()

            self.__apps.remove(_app)
        else:
            for _app in reversed(self.__apps):
                _app['thread']._stop()
                _app['treaad'].join()
                self.__apps.remove(_app)

    def launch_app(self, app_name):
        pass



