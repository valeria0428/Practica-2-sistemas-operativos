import logging
import os
import threading

from kernel.main import KernelMain


class System:
    __kernel_thread = None

    def start_system(self):
        # boot
        self.__file_system_check__()
        self.__starting_kernel__()

    def __file_system_check__(self):
        logging.info("Checking file system...")
        if not os.path.exists('./storage'): # Check if file system exists
            logging.warning("File system is not founded any previous file is deleted")
            try:
                os.mkdir('./storage')
            except Exception as err:
                logging.critical(err)
                os._exit(os.EX_CANTCREAT)

            if os.path.exists('./storage'):
                logging.info("File system created")

        logging.info("File system checked all good")

    def __starting_kernel__(self):
        logging.info("Starting kernel...")
        kernel = KernelMain()
        self.__kernel_thread = threading.Thread(name="kernel", target=kernel.start_system)

        try:
            self.__kernel_thread.start()
        except Exception as err:
            logging.critical("Error starting the kernel system... exited")
            os._exit(os.EX_OSERR)

        self.__kernel_thread.join()
        logging.info("Program finished. Exit code 0")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(threadName)s:.:%(levelname)s] x %(message)s',
                        datefmt="%Y/%m/%d %I:%M:%S %p")
    logging.info("BIOS starting checking system and shooting kernel")
    System().start_system()
