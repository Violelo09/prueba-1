"""
Módulo para manejo de usuarios y autenticación
Gestiona el inicio de sesión y validación de credenciales
"""

def leer_usuarios():
    """
    Lee el archivo usuarios.csv y retorna una lista de diccionarios
    Cada diccionario representa un usuario con sus datos
    """
    usuarios = []
    try:
        # Abrir el archivo en modo lectura
        with open("usuarios.csv", "r", encoding="utf-8") as archivo:
            # Leer la primera línea (encabezados)
            encabezados = archivo.readline().strip().split(",")
            
            # Leer cada línea restante
            for linea in archivo:
                linea = linea.strip()
                if linea:  # Si la línea no está vacía
                    # Separar los valores por coma
                    valores = linea.split(",")
                    # Crear un diccionario con los datos del usuario
                    usuario = {}
                    for i, encabezado in enumerate(encabezados):
                        usuario[encabezado] = valores[i]
                    usuarios.append(usuario)
    except FileNotFoundError:
        print("Error: No se encontró el archivo usuarios.csv")
    except Exception as e:
        print(f"Error al leer usuarios: {e}")
    
    return usuarios


def validar_credenciales(usuario, contrasena):
    """
    Valida si el usuario y contraseña coinciden con algún usuario en el CSV
    Retorna True si las credenciales son correctas, False en caso contrario
    """
    usuarios = leer_usuarios()
    
    # Buscar un usuario que coincida con el nombre y contraseña
    for u in usuarios:
        if u["usuario"] == usuario and u["contrasena"] == contrasena:
            return True
    
    return False


def iniciar_sesion():
    """
    Función principal para iniciar sesión
    Solicita usuario y contraseña, valida y permite máximo 3 intentos
    Retorna True si el login es exitoso, False si se agotan los intentos
    """
    intentos = 0
    max_intentos = 3
    
    print("\n" + "="*50)
    print("SISTEMA DE GESTIÓN TECHLAB - INICIO DE SESIÓN")
    print("="*50)
    
    # Ciclo para permitir hasta 3 intentos
    while intentos < max_intentos:
        print(f"\nIntento {intentos + 1} de {max_intentos}")
        
        # Solicitar credenciales
        usuario = input("Usuario: ")
        contrasena = input("Contraseña: ")
        
        # Validar credenciales
        if validar_credenciales(usuario, contrasena):
            print("\n✓ Inicio de sesión exitoso!")
            return True
        else:
            intentos += 1
            intentos_restantes = max_intentos - intentos
            if intentos_restantes > 0:
                print(f"\n✗ Credenciales incorrectas. Te quedan {intentos_restantes} intento(s).")
            else:
                print("\n✗ Credenciales incorrectas. Se agotaron los intentos.")
                print("Cerrando el programa...")
                return False
    
    return False

