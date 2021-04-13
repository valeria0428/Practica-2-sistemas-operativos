import time
import logging
import threading

from multiprocessing.dummy.connection import Connection
from apps.generate_ramdom_numbers import Main as random_app


class ApplicationsMain:
    __pipe = None  # Extremo de la tubería para el envío de mensajes
    __apps = []  # Aplicaciones activas en el sistema

    def __init__(self, pipe: Connection):
        self.__pipe = pipe  # Se recibe el extremo de la tubería

    def start(self):
        self.listen_messages()  # Se inicia la escucha de mensajes entrantes por la tubería

    def listen_messages(self):
        while True:
            if not self.__pipe.poll(3):  # Se espera a una nueva conexión entrante por la tubería cada 3 segundos
                time.sleep(0.2)  # Se esperan otros 2 milisegundos
                continue # Se continua con el ciclo

            message = self.__pipe.recv()  # Se recibe el mensaje entrante por la tubería

            message = message.split(':')  # Se parte el mensaje entrante para determinar la acción

            if len(message) == 0 and message[0] == "halt":  # Se define la acción para el mensaje halt
                self.__pipe.send({  # Se le responde al kernel la acción de detener las aplicaciones
                    "cmd": "stop",
                    "src": "applications",
                    "dst": "kernel",
                    "msg": "Stopped by user"
                })
                self.halt_apps()  # Se inicia la detención de las aplicaciones
            else:
                if message[0] == "launch":  # Se defina la acción para lanzar una nueva aplicación
                    self.launch_app(message[1])  # Se llama al lanzador de aplicaciones
                if message[0] == "list":  # Se define la acción para listar una nueva aplicación
                    self.list_apps()  # Se llama al método que lista las aplicaciones
                if message[0] == "stop":  # Se define la acción para detener una aplicación
                    self.halt_apps(message[1])  # Se llama al metodo para detener una aplicación

    def list_apps(self):
        apps = [f"{app['pid']} - {app['thread'].getName()}" for app in self.__apps]  # Se itera sobre las aplicaciones separandolas por el nombre
        self.__pipe.send({  # Se envía las aplicaciones
            "cmd": "info",
            "src": "applications",
            "dst": "GUI",
            "msg": apps
        })

    def halt_apps(self, app=None):
        if app:
            _app = next((__app for __app in self.__apps if __app['pid'] == int(app)), None)  # Se itera sobre las aplicaciones para encontrar la solicitada
            if _app is None:  # Si no se encuentra la aplicación se lanza un error
                logging.error("Thread not founded")
                return

            _app['app'].stop()  # Se detiene la aplicación llamando al método stop de la clase system
            _app['thread'].join()  # Se detiene la aplicación llamando al método stop de la clase system

            self.__apps.remove(_app)  # Se remueve del arreglo de aplicaciones
        else:
            for _app in reversed(self.__apps):  # Se itera de forma reversa sobre las aplicaciones
                _app['app'].stop()  # Se detiene la aplicación llamando al método stop de la clase system
                _app['thread'].join()  # Se detiene la aplicación llamando al método stop de la clase system
                self.__apps.remove(_app)  # Se remueve del arreglo de aplicaciones

    def launch_app(self, app_name):
        if app_name == "random":  # Nombre de la aplicación a lanzar
            app = random_app()  # Se llama a la aplicación
            thread = threading.Thread(name=f"application/random{len(self.__apps)}", target=app.random_app, args=[self.__pipe])  # Se declara la aplicación en un nuevo hilo
            thread.start()  # Se inicia la ejecución de la aplicación

            self.__apps.append({   # Se añade al arreglo de aplicaciones
                "pid": thread.native_id,
                "app": app,
                "thread": thread
            })



