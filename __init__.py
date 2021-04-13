import logging
import os
import threading

from kernel.main import KernelMain


class System:
    __kernel_thread = None  # Hilo principal para controlar

    def start_system(self):
        # boot
        self.__file_system_check__()  # Se chekea los sistemas de archivos
        self.__starting_kernel__()  # Se inicia el kernel

    def __file_system_check__(self):
        logging.info("Checking file system...")
        if not os.path.exists('./storage'): # Check if file system exists
            logging.warning("File system is not founded any previous file is deleted")
            try:
                os.mkdir('./storage')  # Si no existe la carpeta de almacenamiento se crea
            except Exception as err:
                logging.critical(err)  # En caso de que suceda un error se anuncia y se mata el sistema
                os._exit(os.EX_CANTCREAT)

            if os.path.exists('./storage'):  # Se verifica si se creo correctamente
                logging.info("File system created")

        logging.info("File system checked all good")

    def __starting_kernel__(self):
        logging.info("Starting kernel...")
        kernel = KernelMain()  # Se define el kernel
        self.__kernel_thread = threading.Thread(name="kernel", target=kernel.start_system)  # Se declara el hilo de ejecución del kernel

        try:
            self.__kernel_thread.start()  # Se inicial el hilo del kernel
        except Exception as err:
            logging.critical("Error starting the kernel system... exited")
            os._exit(os.EX_OSERR)  # En caso de que el kernel no inicie se detiene el systema

        self.__kernel_thread.join()
        logging.info("Program finished. Exit code 0")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(threadName)s:.:%(levelname)s] x %(message)s',
                        datefmt="%Y/%m/%d %I:%M:%S %p")
    logging.info("BIOS starting checking system and shooting kernel")
    System().start_system()
