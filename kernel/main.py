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
    __GUI_CONN, __GUI_CONN_CHILD = None, None
    __FILE_SYSTEM_CONN, __FILE_SYSTEM_CONN_CHILD = None, None
    __APPLICATION_CONN, __APPLICATION_CONN_CHILD = None, None

    __GUI_thread = None
    __FILE_SYSTEM_thread = None
    __APPLICATION_thread = None

    _kernel_status = True

    def start_system(self):
        # Communication Pipes
        self.__GUI_CONN, self.__GUI_CONN_CHILD = Pipe()
        self.__FILE_SYSTEM_CONN, self.__FILE_SYSTEM_CONN_CHILD = Pipe()
        self.__APPLICATION_CONN, self.__APPLICATION_CONN_CHILD = Pipe()

        # Modules
        gui = GUIMain(self.__GUI_CONN_CHILD)
        file_system = FileSystemMain(self.__FILE_SYSTEM_CONN_CHILD)
        application = ApplicationsMain(self.__APPLICATION_CONN_CHILD)

        # Threads instances
        self.__GUI_thread = threading.Thread(name="GUI", target=gui.start)
        self.__FILE_SYSTEM_thread = threading.Thread(name="File System", target=file_system.start)
        self.__APPLICATION_thread = threading.Thread(name="Application", target=application.start)

        logging.info("Kernel ready stating modules...")

        self.__FILE_SYSTEM_thread.start()
        self.__APPLICATION_thread.start()
        self.__GUI_thread.start()

        logging.info("Kernel ready starting system...")
        self.internal()

    def listen_pipes(self, conn: Connection):
        while True:
            if not conn.poll(3):
                time.sleep(0.2)
                continue

            message = conn.recv()
            
            if 'cmd' in message:
                # Tunel messages
                if message['cmd'] == "send":
                    self.find_destination(message)
                elif message['cmd'] == "info":
                    self.find_destination(message)
                elif message['cmd'] == "stop":
                    self.find_destination(message, action="stop")

            elif 'codterm' in message:
                if message['codterm'] == 0:
                    logging.info("Successes operation")
                elif message['codterm'] == 1:
                    logging.warning("Module busy")
                elif message['codterm'] == 2:
                    logging.error(message['msg'])

    def find_destination(self, message, action=None):
        if message['dst'] == "GestorArc":
            self.__FILE_SYSTEM_CONN.send(message['msg'])
        elif message['dst'] == "GUI":
            self.__GUI_CONN.send(message['msg'])
        elif message['dst'] == "applications":
            self.__APPLICATION_CONN.send(message['msg'])
        elif message['dst'] == "kernel":
            if action == "stop":
                self.halt(message['src'])
        else:
            logging.error("Destination not founded")

    def halt(self, instance):
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
        gui_message = threading.Thread(name="kernel/messages/GUI", target=self.listen_pipes, args=[self.__GUI_CONN])
        files_message = threading.Thread(name="kernel/messages/files", target=self.listen_pipes,
                                         args=[self.__FILE_SYSTEM_CONN])
        application_message = threading.Thread(name="kernel/messages/application", target=self.listen_pipes,
                                               args=[self.__APPLICATION_CONN])

        gui_message.start()
        files_message.start()
        application_message.start()

        while self._kernel_status:

            time.sleep(0.2)

        gui_message._stop()
        files_message._stop()
        application_message._stop()
