# Sistema de Gestión de Tareas

Este proyecto implementa una API REST simple para la gestión de tareas con autenticación de usuarios y un cliente de consola para interactuar con ella.

## Requisitos Previos

- Python 3.x instalado en tu sistema.
- `pip` (el gestor de paquetes de Python), que usualmente viene incluido con Python.

## Instalación de Dependencias

El proyecto incluye un archivo `requirements.txt` que lista todas las librerías necesarias.

Para instalarlas, abre una terminal (CMD, PowerShell, Terminal de Linux, etc.) en la carpeta del proyecto y ejecuta el siguiente comando:

```bash
pip install -r requirements.txt
```

Este comando leerá el archivo e instalará automáticamente Flask, Flask-SQLAlchemy, bcrypt y requests en tu sistema.


## Ejecución del Proyecto
Una vez instaladas las dependencias, necesitarás tener **dos terminales** abiertas en la carpeta del proyecto.

**Terminal 1: Iniciar el Servidor**
En la primera terminal, ejecuta el siguiente comando para iniciar la API:
1.  Inicia el servidor Flask:
    ```
    python servidor.py
    ```
El servidor se iniciará, creará la base de datos si no existe, y estará listo para recibir peticiones. Deberías ver un mensaje indicando que el servidor está corriendo en http://127.0.0.1:5000.

**Terminal 2: Ejecutar el Cliente**
En la segunda terminal, ejecuta el cliente de consola para empezar a usar el sistema:
1.  Ejecuta el cliente de consola para interactuar con la API:
    ```
    python cliente.py
    ```
¡Y listo! Ahora puedes seguir las instrucciones del menú en la consola para registrarte, iniciar sesión y gestionar tus tareas.