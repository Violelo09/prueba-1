import usuarios
import equipos
import prestamos
import reportes
# Estas importaciones permiten usar funciones que están en otros archivos:
# - usuarios.py
# - equipos.py
# - prestamos.py
# - reportes.py
# Así el programa está organizado y no todo junto.
# Cada archivo se encarga de una parte del sistema.

def mostrar_menu_principal():
    """
    Muestra el menú principal del sistema
    """
    print("\n" + "="*60)
    print("SISTEMA DE GESTIÓN TECHLAB - MENÚ PRINCIPAL")
    print("="*60)
    print("\n1. Gestión de Equipos")
    print("2. Gestión de Préstamos")
    print("3. Consultar Historial")
    print("4. Exportar Reporte CSV")
    print("5. Salir")
    print("\n" + "-"*60)
    # Esta función solo muestra las opciones principales al usuario.

def menu_equipos():
    """
    Submenú para gestión de equipos
    """
    while True:
        # Este while True repite el menú hasta que el usuario decida volver.
        print("\n" + "="*50)
        print("GESTIÓN DE EQUIPOS")
        print("="*50)
        print("\n1. Registrar nuevo equipo")
        print("2. Listar todos los equipos")
        print("3. Consultar equipo por ID")
        print("4. Volver al menú principal")
        
        opcion = input("\nSeleccione una opción (1-4): ").strip()
        # Aquí el usuario elige lo que quiere hacer.

        if opcion == "1":
            equipos.registrar_equipo() 
            # Llama a la función del archivo equipos.py
        elif opcion == "2":
            equipos.listar_equipos()
        elif opcion == "3":
            equipos.consultar_equipo()
        elif opcion == "4":
            break  # Sale del submenú y regresa al menú principal
        else:
            print("\n✗ Opción inválida. Por favor seleccione una opción válida.")
            # Si escribe algo incorrecto, le muestra este mensaje.

def menu_prestamos():
    """
    Submenú para gestión de préstamos
    """
    while True:
        print("\n" + "="*50)
        print("GESTIÓN DE PRÉSTAMOS")
        print("="*50)
        print("\n1. Registrar solicitud de préstamo")
        print("2. Aprobar/Rechazar préstamo")
        print("3. Registrar devolución de equipo")
        print("4. Volver al menú principal")
        
        opcion = input("\nSeleccione una opción (1-4): ").strip()

        if opcion == "1":
            prestamos.registrar_solicitud_prestamo()
            # Registrar cuando un usuario pide un equipo.
        elif opcion == "2":
            prestamos.aprobar_rechazar_prestamo()
            # Para decidir si se aprueba o se rechaza la solicitud.
        elif opcion == "3":
            prestamos.registrar_devolucion()
            # Para registrar cuándo devuelven un equipo.
        elif opcion == "4":
            break
            # Regresa al menú principal
        else:
            print("\n✗ Opción inválida. Por favor seleccione una opción válida.")

def main():
    """
    Función principal del programa
    Maneja el flujo completo: login -> menú principal -> opciones
    """
    # Primero se hace el inicio de sesión
    if not usuarios.iniciar_sesion():
        return  
        # Si iniciar_sesion() devuelve False, el programa se termina.

    # Si el login fue correcto, se entra al menú principal
    while True:
        mostrar_menu_principal()  
        opcion = input("Seleccione una opción (1-5): ").strip()

        if opcion == "1":
            menu_equipos()  # Va al submenú de equipos
        elif opcion == "2":
            menu_prestamos()  # Va al submenú de préstamos
        elif opcion == "3":
            prestamos.consultar_historial()
            # Consultar todos los préstamos hechos antes
        elif opcion == "4":
            reportes.exportar_reporte_csv()
            # Crea un archivo CSV con la información del sistema
        elif opcion == "5":
            # Mensaje de salida
            print("\n" + "="*60)
            print("Gracias por usar el Sistema de Gestión TechLab")
            print("¡Hasta pronto!")
            print("="*60)
            break  
            # Cierra el programa
        else:
            print("\n✗ Opción inválida. Por favor seleccione una opción válida.")

# Punto de entrada del programa
if __name__ == "__main__":
    main()
    # Esto significa:
    # "Si este archivo se ejecuta directamente, correr la función main()"
    # Es la forma correcta de iniciar un programa en Python.
