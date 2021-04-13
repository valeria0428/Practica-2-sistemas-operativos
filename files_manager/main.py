import os
import logging
import time
import json
from multiprocessing.dummy.connection import Connection


class FileSystemMain:
    __pipe = None  # Extremo de la tubería para recibir y enviar mensajes
    __files = None  # Archivos en el sistema de archivos
    __dirs = None  # Directorios existentes en el sistema de archivos
    __total = 0  # Peso total de los archivos en el sistema de archivos

    def __init__(self, pipe: Connection):
        self.__pipe = pipe  # Se recibe el extremo de la tubería

    def start(self):  # Se inician los métodos para cargar el sistema
        logging.info("Reading directories")
        self.load_files()
        self.listen_messages()

    def load_files(self):
        for root, dirs, files in os.walk("./storage"):  # Se cargan los archivos en el sistema
            self.__dirs = [name for name in dirs]  # Se itera sobre los directorios
            self.__files = [name for name in files]  # Se itera en busca de archivos
            self.__total = sum(os.path.getsize(os.path.join(root, name)) for name in files)  # Se suma el total de peso de los archivos

        logging.info(f"Files loaded. Total: {self.__total}")

    def listen_messages(self):
        logging.info("Files manager started - Redirecting outputs to logger file")
        new_handler = logging.FileHandler('./storage/logs', 'a')  # Se crea un nuevo manejador para logging
        formatter = logging.Formatter('%(asctime)s [%(threadName)s:.:%(levelname)s] x %(message)s',
                                      "%Y/%m/%d %I:%M:%S %p")  # Se le da un formato al logging
        new_handler.setFormatter(formatter)  # Se une el manejador con el formato
        log = logging.getLogger()  # Se obtiene el logger actual
        for hdlr in log.handlers[:]:
            log.removeHandler(hdlr)  # Retira los controladores del logger actual
        log.addHandler(new_handler)  # Se añade el nuevo controlador

        while True:  # Ciclo infinito para mantener la escucha activa
            if not self.__pipe.poll(3):  # Se espera por la llegada de un nuevo mensaje cada 3 segundos
                time.sleep(0.2)  # Y se espera dos milisegundos por cada iteración
                continue

            message = self.__pipe.recv()  # Se recibe el mensaje entrante
            message = message.split(':')  # Se parte el mensaje entre el comando y la información dentro del mensaje

            if message[0].lower() == 'log':  # Se define las acciones para log
                logging.info(message[1])

            if message[0].lower() == 'read':  # Se define la acción de leer el log
                with open('./storage/logs', "r") as logs:  # Se abre el archivo de log
                    lines = logs.readlines()  # Se lee todas las lineas
                    last_lines = lines[-10:]  # Se obtiene las ultimas 10 lineas
                    self.__pipe.send({  # Se envía la información
                        "cmd": "info",
                        "src": "GestorArc",
                        "dst": "GUI",
                        "msg": last_lines
                    })

            if message[0].lower() == 'folder':  # Se define la acción de administrar un folder
                self.manage_folders(int(message[1]), message[2])  # Se llama el método para manejar los folders

    def manage_folders(self, operation, name):
        if operation == 0:
            os.mkdir(f'./storage/{name}')  # Se crea el folder especificado
        elif operation == 1:
            os.rmdir(f'./storage/{name}')  # Se borra el directorio especificado