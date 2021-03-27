import random
import time

from multiprocessing.dummy.connection import Connection


def random_app(pipe: Connection):
    status = True
    while status:
        rand = random.randint(0, 1000) % 10
        pipe.send({
            "cmd": "send",
            "src": "application/random1",
            "dst": "GestorArc",
            "msg": f"log:Numero generado {rand}"
        })

        if rand > 30 and rand < 40:
            status = False
            pipe.send({
                "codterm": 2,
                "msg": "Bad description"
            })

        if rand > 10 and rand < 20:
            raise Exception("Divide by 0")

        time.sleep(5)