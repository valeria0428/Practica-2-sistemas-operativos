import random
import time

from multiprocessing.dummy.connection import Connection
from system import System


# Aplicación de prueba
class Main(System):  # Se hereda de system
    def random_app(self, pipe: Connection):
        while self.running:
            rand = random.randint(0, 1000) % 10  # Se genera un numero aleatorio
            pipe.send({  # Se envia el numero generado para ser registrado en el log
                "cmd": "send",
                "src": "application/random1",
                "dst": "GestorArc",
                "msg": f"log:Numero generado {rand}"
            })

            if rand > 30 and rand < 40:  # Si esta en el intervalo de (30, 40) Se genera un error
                self.running = False
                pipe.send({
                    "codterm": 2,
                    "msg": "Bad description"
                })

            if rand > 10 and rand < 20:  # Si esta en el intervalo de (10, 20) Se genera un error
                raise Exception("Divide by 0")

            time.sleep(5)
