import random
import time

from multiprocessing.dummy.connection import Connection
from system import System


class Main(System):
    def random_app(self, pipe: Connection):
        while self.running:
            rand = random.randint(0, 1000) % 10
            pipe.send({
                "cmd": "send",
                "src": "application/random1",
                "dst": "GestorArc",
                "msg": f"log:Numero generado {rand}"
            })

            if rand > 30 and rand < 40:
                self.running = False
                pipe.send({
                    "codterm": 2,
                    "msg": "Bad description"
                })

            if rand > 10 and rand < 20:
                raise Exception("Divide by 0")

            time.sleep(5)