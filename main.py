"""
Sistema de Gestión de Inventario TechLab
Aplicación de consola para gestionar equipos tecnológicos y préstamos
"""

import usuarios
import equipos
import prestamos
import reportes


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


def menu_equipos():
    """
    Submenú para gestión de equipos
    """
    while True:
        print("\n" + "="*50)
        print("GESTIÓN DE EQUIPOS")
        print("="*50)
        print("\n1. Registrar nuevo equipo")
        print("2. Listar todos los equipos")
        print("3. Consultar equipo por ID")
        print("4. Volver al menú principal")
        
        opcion = input("\nSeleccione una opción (1-4): ").strip()
        
        if opcion == "1":
            equipos.registrar_equipo()
        elif opcion == "2":
            equipos.listar_equipos()
        elif opcion == "3":
            equipos.consultar_equipo()
        elif opcion == "4":
            break
        else:
            print("\n✗ Opción inválida. Por favor seleccione una opción válida.")


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
        elif opcion == "2":
            prestamos.aprobar_rechazar_prestamo()
        elif opcion == "3":
            prestamos.registrar_devolucion()
        elif opcion == "4":
            break
        else:
            print("\n✗ Opción inválida. Por favor seleccione una opción válida.")


def main():
    """
    Función principal del programa
    Maneja el flujo completo: login -> menú principal -> opciones
    """
    # Iniciar sesión
    if not usuarios.iniciar_sesion():
        return  # Si el login falla, terminar el programa
    
    # Ciclo principal del menú
    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione una opción (1-5): ").strip()
        
        if opcion == "1":
            menu_equipos()
        elif opcion == "2":
            menu_prestamos()
        elif opcion == "3":
            prestamos.consultar_historial()
        elif opcion == "4":
            reportes.exportar_reporte_csv()
        elif opcion == "5":
            print("\n" + "="*60)
            print("Gracias por usar el Sistema de Gestión TechLab")
            print("¡Hasta pronto!")
            print("="*60)
            break
        else:
            print("\n✗ Opción inválida. Por favor seleccione una opción válida.")


# Punto de entrada del programa
if __name__ == "__main__":
    main()

