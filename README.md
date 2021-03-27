# Practica 2
En esta práctica se utiliza diferentes conceptos del manejo
hilos para lograr una operación exitosa entre diferentes modulos de un sistema.

## Especificaciones
Para este proyecto no se usó ninguna librería externa más alla
de las incluidas con python.

Para iniciar el programar basta con correr el archivo `__init__.py`

## Integrantes
**Valeria Castro Guzmán** - **202019413010**

## Conceptos
Para generar los diferentes procesos dentro del sistema
se crearon 4 modulos cada uno con funciones totalmente
independientes de los demas.

El inicio del programa es un proceso al cual denomine BIOS
consiste en verificar que la carpeta storage(La cual simula
el disco duro) este disponible y si no lo esta es creada, a
su vez se tiene encuenta que no existe ningún problema a
la hora de agregar la carpeta al sistema.

Posterior a esto se inicia el kernel el cual se encarga
de crear todas las tuberías de comunicación que son utilizadas
para hablar entre los modulos. Además de tener todos los
hilos necesarios para escuchar a estas y levantar los
modulos faltantes

![pipes](https://www.python-course.eu/images/named_pipes.png)
---
Luego de esto todos los modulos son levantados donde estos
reciben el otro extremo de la tubería y se encuentran preparados
para atender cualquier mensaje entrante o enviar mensajes en caso
de que sea necesario.

### Logs
Los logs del sistema se encuentran guardados dentro del
almacenamiento del sistema en un archivo llamado logs.


**Universidad EAFIT - 2021 | Sistemas Operativos**