import time
import threading

from multiprocessing.dummy.connection import Connection
from GUI.interface import Interface


class GUIMain:
    __pipe: Connection = None  # Se declara la variable para la tubería entrante
    __thread = None  # Se declara el hilo de ejecución de la escucha de mensajes

    def __init__(self, pipe):
        self.__pipe = pipe  # Se recibe la tubería

    def listen_messages(self):
        while True:
            if not self.__pipe.poll(3):
                time.sleep(0.2)
                continue

    def wait(self):
        while not self.__pipe.poll(3):  # Se espera por una conexión entrante cada 3 segundos
            continue

    def start(self):
        self.__thread = threading.Thread(name="GUI/Messages", target=self.listen_messages)  # Se inicializa la escucha de mensajes
        self.__thread.start()  # Se inicia el hilo de escucha de mensajes

        interface = Interface()  # Se instancia la clase interfaz donde están todas las interfaces estandarizadas
        option = 0  # Se declara la selección del usuario
        
        time.sleep(2)  # Se espera dos segundos
        while True:
            if option != 1:
                interface.main()  # Se llama al main
                option = interface.input()  # Se llama al metodo de entrada de la interfaz

                if option == 4:  # Acciones al seleccionar la opción 4
                    self.__pipe.send({
                        'cmd': "info",
                        'src': "GUI",
                        'dst': 'kernel',
                        'msg': "sysinfo"
                    })

                    self.wait()  # Se espera por la respuesta del modulo solicitado

                    information = self.__pipe.recv()  # Se recibe el mensaje por parte del modulo
                    _, option = interface.decide_option(option, 0, information['msg'])  # Se decide la opción de impresión de la interfaz según la opción

                elif option == 2:  # Acción al seleccionar la opción 2
                    self.__pipe.send({
                        'cmd': 'info',
                        "src": "GUI",
                        "dst": "GestorArc",
                        "msg": "read"
                    })

                    self.wait()  # Se espera por la respuesta del modulo solicitado

                    information = self.__pipe.recv()  # Se recibe el mensaje por parte del modulo
                    interface.decide_option(option, 0, information)  # Se decide la opción de impresión de la interfaz según la opción

                elif option == 3:
                    _, option = interface.decide_option(option, 0)  # Se envía la solicitud de la información adicional
                    self.__pipe.send({
                        'cmd': "info",
                        'src': "GUI",
                        "dst": "GestorArc",
                        "msg": f"folder:0:{_}"
                    })
                else:
                    interface.decide_option(option, 0)  # Se envía la solicitud de la información adicional
            else:
                option = interface.input()  # Se solicita la entrada de opción a la interfaz
                if option == 1:  # Se selecciona la opción 1
                    _, option = interface.decide_option(option, 1)  # Se decide la acción de la interfaz
                    self.__pipe.send({
                        "cmd": "info",
                        "src": "GUI",
                        "dst": "applications",
                        "msg": f"launch:{_}"
                    })
                    option = 0
                elif option == 2:  # Se selecciona la opción 2
                    self.__pipe.send({
                        "cmd": "info",
                        "src": "GUI",
                        "dst": "applications",
                        "msg": f"list"
                    })
                    self.wait()  # Se espera la respuesta del modulo solicitado
                    information = self.__pipe.recv()  # Se recibe la información del modulo
                    interface.decide_option(option, 1, information)  # Se envía la solicitud de la información adicional
                elif option == 3:
                    _, option = interface.decide_option(option, 1)  # Se decide la acción
                    self.__pipe.send({
                        "cmd": "info",
                        "src": "GUI",
                        "dst": "applications",
                        "msg": f"stop:{_}"
                    })
                else:
                    interface.decide_option(option, 1)  # Se decide la acción

            print()  # Se deja un espacio por estética
            time.sleep(2)  # Se espera 2 segundos
