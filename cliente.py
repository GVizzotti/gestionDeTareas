# cliente.py
import requests
import getpass

BASE_URL = "http://localhost:5000"
#sesión para las cookies de login 
sesion_api = requests.Session()

def procesar_respuesta_api(respuesta):
    """Función centralizada para mostrar mensajes de éxito o error."""
    if respuesta.ok: 
        try:
            # mensaje JSON si existe
            datos = respuesta.json()
            print(f"Éxito: {datos.get('mensaje', 'Operación completada.')}")
        except requests.exceptions.JSONDecodeError:
            # Si no es JSON muestra el texto
            print("Respuesta del servidor recibida:")
            print("-" * 20)
            print(respuesta.text)
            print("-" * 20)
    else:
        try:
            datos = respuesta.json()
            print(f"Error: {datos.get('error', 'Error desconocido.')} (Código: {respuesta.status_code})")
        except requests.exceptions.JSONDecodeError:
            print(f"Error en el servidor (Código: {respuesta.status_code})")



def menu_no_autenticado():
    """Muestra el menú para usuarios que no han iniciado sesión."""
    print("\nMENÚ PRNCIPAL")
    print("1. Registrar un nuevo usuario")
    print("2. Iniciar sesión")
    print("3. Salir")
    opcion = input("Seleccione una opción: ")

    if opcion == '1':
        usuario = input("Ingrese su nuevo nombre de usuario: ")
        contrasenia = getpass.getpass("Ingrese su contraseña: ")
        respuesta = sesion_api.post(f"{BASE_URL}/registro", json={"usuario": usuario, "contrasenia": contrasenia})
        procesar_respuesta_api(respuesta)
        return False 

    elif opcion == '2':
        usuario = input("Usuario: ")
        contrasenia = getpass.getpass("Contraseña: ")
        respuesta = sesion_api.post(f"{BASE_URL}/login", json={"usuario": usuario, "contrasenia": contrasenia})
        procesar_respuesta_api(respuesta)
        return respuesta.ok 

    elif opcion == '3':
        return "salir" 

    else:
        print("Opción no válida. Intente de nuevo.")
        return False



def menu_autenticado():
    """Muestra el menú para usuarios que ya iniciaron sesión."""
    print("\nMENÚ DEL USUARIO")
    print("1. Ver mis tareas")
    print("2. Crear una nueva tarea")
    print("3. Cerrar sesión")
    opcion = input("Seleccione una opción: ")

    if opcion == '1':
        respuesta = sesion_api.get(f"{BASE_URL}/tareas")
        procesar_respuesta_api(respuesta)
        return True

    elif opcion == '2':
        titulo = input("Título de la tarea: ")
        descripcion = input("Descripción (opcional): ")
        respuesta = sesion_api.post(f"{BASE_URL}/tareas", json={"titulo": titulo, "descripcion": descripcion})
        procesar_respuesta_api(respuesta)
        return True

    elif opcion == '3':
        respuesta = sesion_api.post(f"{BASE_URL}/logout")
        procesar_respuesta_api(respuesta)
        return False 

    else:
        print("Opción no válida. Intente de nuevo.")
        return True

def main():
    """Función principal que ejecuta el cliente de consola."""
    print("Bienvenido al Cliente del Sistema de Gestión de Tareas")
    autenticado = False

    while True:
        try:
            if not autenticado:
                resultado_menu = menu_no_autenticado()
                if resultado_menu == "salir":
                    break
                autenticado = resultado_menu
            else:
                autenticado = menu_autenticado()

        except requests.exceptions.ConnectionError:
            print("\n CRÍTICO: No se pudo conectar al servidor. Asegúrese de que `servidor.py` esté en ejecución.")
            break
        except KeyboardInterrupt:
            print("\nSaliendo del programa...")
            break
        except Exception as e:
            print(f"\nHa ocurrido un error inesperado: {e}")
            break

    print("Gracias por usar el sistema. ¡Que tengas un buen día!")

if __name__ == "__main__":
    main()