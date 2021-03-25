import os
import logging


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

    def load_files(self):
        for root, dirs, files in os.walk("./storage"):
            self.__dirs = [name for name in dirs]
            self.__files = [name for name in files]
            self.__total = sum(os.path.getsize(os.path.join(root, name)) for name in files)

        logging.info(f"Files loaded. Total: {self.__total}")
