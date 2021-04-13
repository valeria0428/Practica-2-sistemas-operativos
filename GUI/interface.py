import logging


class Interface:
    def main(self): # Interfaz del menu principal
        print("_________Main_________")
        print("1. Controller applications")
        print("2. See system logs")
        print("3. Create new folder")
        print("4. See system information")

    def controller_applications(self):  # Interfaz de controlador de aplicaciones
        print("_________Controller applications_________")
        print("1. Open new application")
        print("2. List running applications")
        print("3. Close application")

    def system_logs(self, logs):  # Imprime los logs
        print("_________Last 10 logs_________")

        for log in logs:  # Itera sobre el arreglo del logs
            print(log)

    def print_application(self, applications):  # Imprime las aplicaciones
        print("_________Applications_________")
        print("PID - Name")

        for application in applications:  # Se itera sobre el arreglo de aplicaciones
            print(application)

    def create_folder(self):
        return input("Insert folder name: ")  # Se solicita el nombre del folder

    def system_information(self, information):  # Se imprime el estado del sistema
        print(f"Kernel: {information['kernel']}")
        print(f"GUI: {information['GUI']}")
        print(f"Applicaciones: {information['applications']}")
        print(f"Files_manager: {information['files_manager']}")

    def input(self):
        return int(input(".:: Eliga una opción: "))  # Se solicita una opción al usuario

    def decide_option(self, option, menu, information=None):
        # Se llama los métodos según la decisión del usuario
        if menu == 0:
            if option == 1:
                self.controller_applications()
                return None, 1
            elif option == 2:
                self.system_logs(information)
                return None, 2
            elif option == 3:
                return self.create_folder(), 3
            elif option == 4:
                self.system_information(information)
                return None, 4
        elif menu == 1:
            if option == 1:
                return input(".:: Insert application name: "), 1
            elif option == 2:
                self.print_application(information), 2
            elif option == 3:
                return input(".:: Insert application PID: "), 3
        else:
            logging.error("The selected menu dosen't exists")