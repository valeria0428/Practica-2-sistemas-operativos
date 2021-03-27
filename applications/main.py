import time
import json
import logging
import threading

from multiprocessing.dummy.connection import Connection
from apps.generate_ramdom_numbers import Main as random_app


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
                if message[0] == "list":
                    self.list_apps()
                if message[0] == "stop":
                    self.halt_apps(message[1])

    def list_apps(self):
        apps = [f"{app['pid']} - {app['thread'].getName()}" for app in self.__apps]
        self.__pipe.send({
            "cmd": "info",
            "src": "applications",
            "dst": "GUI",
            "msg": apps
        })

    def halt_apps(self, app=None):
        if app:
            _app = next((__app for __app in self.__apps if __app['pid'] == int(app)), None)
            if _app is None:
                logging.error("Thread not founded")
                return

            _app['app'].stop()
            _app['thread'].join()

            self.__apps.remove(_app)
        else:
            for _app in reversed(self.__apps):
                _app['app'].stop()
                _app['thread'].join()
                self.__apps.remove(_app)

    def launch_app(self, app_name):
        if app_name == "random":
            app = random_app()
            thread = threading.Thread(name=f"application/random{len(self.__apps)}", target=app.random_app, args=[self.__pipe])
            thread.start()

            self.__apps.append({
                "pid": thread.native_id,
                "app": app,
                "thread": thread
            })



