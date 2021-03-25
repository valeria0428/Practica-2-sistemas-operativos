import logging
import time
import threading

from multiprocessing import Pipe

# System parts
from applications.main import ApplicationsMain
from files_manager.main import FileSystemMain
from GUI.main import GUIMain


class KernelMain:
    __GUI_CONN, __GUI_CONN_CHILD = None, None
    __FILE_SYSTEM_CONN, __FILE_SYSTEM_CONN_CHILD = None, None
    __APPLICATION_CONN, __APPLICATION_CONN_CHILD = None, None

    __GUI_thread = None
    __FILE_SYSTEM_thread = None
    __APPLICATION_thread = None

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

    def listen_pies(self):
        gui_message = self.__GUI_CONN.poll(3)
        application_message = self.__APPLICATION_CONN.poll(3)
        file_system_message = self.__FILE_SYSTEM_CONN.poll(3)

    def internal(self):
        while True:
            time.sleep(0.2)