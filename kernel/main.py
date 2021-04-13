import logging
import threading
import time
import json

from multiprocessing import Pipe
from multiprocessing.dummy.connection import Connection
# System parts

from GUI.main import GUIMain
from applications.main import ApplicationsMain
from files_manager.main import FileSystemMain


class KernelMain:
    # Se declara las conexiones de todas las tuberías de los modulos del sistema
    __GUI_CONN, __GUI_CONN_CHILD = None, None
    __FILE_SYSTEM_CONN, __FILE_SYSTEM_CONN_CHILD = None, None
    __APPLICATION_CONN, __APPLICATION_CONN_CHILD = None, None

    # Se declara las variables de los hilos de los diferentes modulos
    __GUI_thread = None
    __FILE_SYSTEM_thread = None
    __APPLICATION_thread = None

    # Status actual del kernel del sistema
    _kernel_status = True

    def start_system(self):
        # Communication Pipes --> Se inicializan las tuberias
        self.__GUI_CONN, self.__GUI_CONN_CHILD = Pipe()
        self.__FILE_SYSTEM_CONN, self.__FILE_SYSTEM_CONN_CHILD = Pipe()
        self.__APPLICATION_CONN, self.__APPLICATION_CONN_CHILD = Pipe()

        # Modules --> Se inicializan los módulos
        gui = GUIMain(self.__GUI_CONN_CHILD)
        file_system = FileSystemMain(self.__FILE_SYSTEM_CONN_CHILD)
        application = ApplicationsMain(self.__APPLICATION_CONN_CHILD)

        # Threads instances --> Se inicializan los hilos de los modulos
        self.__GUI_thread = threading.Thread(name="GUI", target=gui.start)
        self.__FILE_SYSTEM_thread = threading.Thread(name="File System", target=file_system.start)
        self.__APPLICATION_thread = threading.Thread(name="Application", target=application.start)

        logging.info("Kernel ready stating modules...")

        # Se inician los hilos que sostienen cada uno de los modulos
        self.__FILE_SYSTEM_thread.start()
        self.__APPLICATION_thread.start()
        self.__GUI_thread.start()

        logging.info("Kernel ready starting system...")
        self.internal()

    def listen_pipes(self, conn: Connection):
        while True:
            if not conn.poll(3):  # Escucha si existe un mensaje entrante por la tubería cada 3 segundos
                time.sleep(0.2)  # Espera dos milisegundos
                continue

            message = conn.recv()  # Se recive el mensaje entrante
            
            if 'cmd' in message: # Se define las acciones para los mensajes
                # Tunel messages
                if message['cmd'] == "send":
                    self.find_destination(message)  # Se encuentra el destinatario del mensaje
                elif message['cmd'] == "info":
                    self.find_destination(message)  # Se obtiene la información en el sistema
                elif message['cmd'] == "stop":
                    self.find_destination(message, action="stop")  # Se envia la orden de frenar determinado modulo al destinatario

            elif 'codterm' in message:  # Acciones de código de terminación
                if message['codterm'] == 0:  # Acción para código de terminación 0
                    logging.info("Successes operation")
                elif message['codterm'] == 1:  # Acción para código de terminación 0
                    logging.warning("Module busy")
                elif message['codterm'] == 2:  # Acción para código de terminación 0
                    logging.error(message['msg'])

    def find_destination(self, message, action=None):
        # Se decide la tuberia de salida del mensaje
        if message['dst'] == "GestorArc":
            self.__FILE_SYSTEM_CONN.send(message['msg'])
        elif message['dst'] == "GUI":
            self.__GUI_CONN.send(message['msg'])
        elif message['dst'] == "applications":
            self.__APPLICATION_CONN.send(message['msg'])
        elif message['dst'] == "kernel":
            if action == "stop":
                self.halt(message['src'])

            if not action:
                if message['msg'] == 'sysinfo':
                    self.__GUI_CONN.send({
                        "cmd": 'info',
                        "src": "kernel",
                        "dst": 'GUI',
                        "msg": {
                            "GUI": self.__GUI_thread.is_alive(),
                            "files_manager": self.__FILE_SYSTEM_thread.is_alive(),
                            "applications": self.__APPLICATION_thread.is_alive(),
                            "kernel": self._kernel_status
                        }
                    })
        else:
            logging.error("Destination not founded")

    def halt(self, instance):
        # Se detiene determinado modulo del sistema
        if instance == "GUI":
            self.__GUI_thread._stop()
            self.__GUI_thread.join()
        elif instance == "applications":
            self.__APPLICATION_thread._stop()
            self.__APPLICATION_thread.join()
        elif instance == "GestorArc":
            self.__FILE_SYSTEM_thread._stop()
            self.__FILE_SYSTEM_thread.join()

    def internal(self):
        # Se declaran los hilos de escucha de las tuberias de cada uno de los modulos
        gui_message = threading.Thread(name="kernel/messages/GUI", target=self.listen_pipes, args=[self.__GUI_CONN])
        files_message = threading.Thread(name="kernel/messages/files", target=self.listen_pipes,
                                         args=[self.__FILE_SYSTEM_CONN])
        application_message = threading.Thread(name="kernel/messages/application", target=self.listen_pipes,
                                               args=[self.__APPLICATION_CONN])

        # Se inicializan los hilos de escucha de las tuberías de cada uno de los modulos
        gui_message.start()
        files_message.start()
        application_message.start()

        # Se mantiene el kernel
        while self._kernel_status:
            time.sleep(0.2)

        gui_message._stop()
        files_message._stop()
        application_message._stop()
