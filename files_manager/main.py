import os
import logging
import time
import json


class FileSystemMain:
    __pipe = None
    __files = None
    __dirs = None
    __total = 0

    def __init__(self, pipe):
        self.__pipe = pipe

    def start(self):
        logging.info("Reading directories")
        self.load_files()
        self.listen_messages()

    def load_files(self):
        for root, dirs, files in os.walk("./storage"):
            self.__dirs = [name for name in dirs]
            self.__files = [name for name in files]
            self.__total = sum(os.path.getsize(os.path.join(root, name)) for name in files)

        logging.info(f"Files loaded. Total: {self.__total}")

    def listen_messages(self):
        logging.info("Files manager started - Redirecting outputs to logger file")
        new_handler = logging.FileHandler('./storage/logs', 'a')
        formatter = logging.Formatter('%(asctime)s [%(threadName)s:.:%(levelname)s] x %(message)s',
                                      "%Y/%m/%d %I:%M:%S %p")
        new_handler.setFormatter(formatter)
        log = logging.getLogger()
        for hdlr in log.handlers[:]:
            log.removeHandler(hdlr)
        log.addHandler(new_handler)

        while True:
            if not self.__pipe.poll(3):
                time.sleep(0.2)
                continue

            message = self.__pipe.recv()
            message = message.split(':')

            if message[0].lower() == 'log':
                logging.info(message[1])

            if message[0].lower() == 'read':
                pass

            if message[0].lower() == 'folder':
                self.manage_folders(message[1], message[2])

    def manage_folders(self, operation, name):
        if operation == 0:
            os.mkdir(f'./storage/{name}')
        elif operation == 1:
            os.rmdir(f'./storage/{name}')