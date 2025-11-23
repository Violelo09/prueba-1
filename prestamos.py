"""
Módulo para gestión de préstamos de equipos
Maneja solicitudes, aprobaciones, rechazos y devoluciones
"""

from datetime import datetime, timedelta
import equipos


def leer_prestamos():
    """
    Lee el archivo prestamos.csv y retorna una lista de diccionarios
    Cada diccionario representa un préstamo con sus datos
    """
    prestamos = []
    try:
        with open("prestamos.csv", "r", encoding="utf-8") as archivo:
            encabezados = archivo.readline().strip().split(",")
            
            for linea in archivo:
                linea = linea.strip()
                if linea:
                    valores = linea.split(",")
                    prestamo = {}
                    for i, encabezado in enumerate(encabezados):
                        prestamo[encabezado] = valores[i]
                    prestamos.append(prestamo)
    except FileNotFoundError:
        print("Error: No se encontró el archivo prestamos.csv")
    except Exception as e:
        print(f"Error al leer préstamos: {e}")
    
    return prestamos


def guardar_prestamos(prestamos):
    """
    Guarda la lista de préstamos en el archivo prestamos.csv
    Recibe una lista de diccionarios con los datos de los préstamos
    """
    try:
        with open("prestamos.csv", "w", encoding="utf-8") as archivo:
            # Escribir encabezados
            encabezados = [
                "prestamo_id", "equipo_id", "nombre_equipo", "usuario_prestatario",
                "tipo_usuario", "fecha_solicitud", "fecha_prestamo", "fecha_devolucion",
                "dias_autorizados", "dias_reales_usados", "retraso", "estado", "mes", "anio"
            ]
            archivo.write(",".join(encabezados) + "\n")
            
            # Escribir cada préstamo
            for prestamo in prestamos:
                valores = [
                    prestamo.get("prestamo_id", ""),
                    prestamo.get("equipo_id", ""),
                    prestamo.get("nombre_equipo", ""),
                    prestamo.get("usuario_prestatario", ""),
                    prestamo.get("tipo_usuario", ""),
                    prestamo.get("fecha_solicitud", ""),
                    prestamo.get("fecha_prestamo", ""),
                    prestamo.get("fecha_devolucion", ""),
                    prestamo.get("dias_autorizados", ""),
                    prestamo.get("dias_reales_usados", ""),
                    prestamo.get("retraso", ""),
                    prestamo.get("estado", ""),
                    prestamo.get("mes", ""),
                    prestamo.get("anio", "")
                ]
                archivo.write(",".join(valores) + "\n")
        
        return True
    except Exception as e:
        print(f"Error al guardar préstamos: {e}")
        return False


def obtener_dias_maximos(tipo_usuario):
    """
    Retorna los días máximos permitidos según el tipo de usuario
    Estudiante: 3 días, Instructor: 7 días, Administrativo: 10 días
    """
    if tipo_usuario.upper() == "ESTUDIANTE":
        return 3
    elif tipo_usuario.upper() == "INSTRUCTOR":
        return 7
    elif tipo_usuario.upper() == "ADMINISTRATIVO":
        return 10
    else:
        return 0


def validar_fecha(fecha_str):
    """
    Valida que la fecha tenga el formato correcto (YYYY-MM-DD)
    Retorna True si es válida, False en caso contrario
    """
    try:
        datetime.strptime(fecha_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def calcular_dias_diferencia(fecha_inicio, fecha_fin):
    """
    Calcula la diferencia en días entre dos fechas
    Recibe fechas en formato string "YYYY-MM-DD"
    Retorna el número de días
    """
    try:
        fecha1 = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fecha2 = datetime.strptime(fecha_fin, "%Y-%m-%d")
        diferencia = fecha2 - fecha1
        return diferencia.days
    except ValueError:
        return 0


def registrar_solicitud_prestamo():
    """
    Permite registrar una nueva solicitud de préstamo
    Valida disponibilidad del equipo y límites de días según tipo de usuario
    """
    print("\n" + "="*50)
    print("REGISTRAR SOLICITUD DE PRÉSTAMO")
    print("="*50)
    
    # Mostrar equipos disponibles
    print("\nEquipos disponibles:")
    equipos_lista = equipos.leer_equipos()
    disponibles = [e for e in equipos_lista if e.get("estado_actual") == "DISPONIBLE"]
    
    if not disponibles:
        print("\n✗ No hay equipos disponibles en este momento.")
        return False
    
    print(f"\n{'ID':<15} {'Nombre':<30} {'Categoría':<20}")
    print("-" * 65)
    for equipo in disponibles:
        print(f"{equipo.get('equipo_id'):<15} {equipo.get('nombre_equipo'):<30} {equipo.get('categoria'):<20}")
    
    # Solicitar datos
    equipo_id = input("\nIngrese el ID del equipo a prestar: ").strip()
    
    # Validar que el equipo existe y está disponible
    equipo = equipos.obtener_equipo_por_id(equipo_id)
    if not equipo:
        print(f"\n✗ Error: No se encontró un equipo con ID '{equipo_id}'")
        return False
    
    if equipo.get("estado_actual") != "DISPONIBLE":
        print(f"\n✗ Error: El equipo '{equipo.get('nombre_equipo')}' no está disponible.")
        print(f"Estado actual: {equipo.get('estado_actual')}")
        return False
    
    # Verificar que no tenga préstamos pendientes sin devolver
    prestamos = leer_prestamos()
    for prestamo in prestamos:
        if (prestamo.get("equipo_id") == equipo_id and 
            prestamo.get("estado") in ["PENDIENTE", "APROBADO"]):
            print(f"\n✗ Error: El equipo tiene un préstamo {prestamo.get('estado').lower()} sin resolver.")
            return False
    
    # Solicitar datos del prestatario
    usuario_prestatario = input("Nombre del usuario prestatario: ").strip()
    
    print("\nTipos de usuario disponibles:")
    print("1. ESTUDIANTE (máximo 3 días)")
    print("2. INSTRUCTOR (máximo 7 días)")
    print("3. ADMINISTRATIVO (máximo 10 días)")
    
    tipo_opcion = input("\nSeleccione el tipo de usuario (1-3): ").strip()
    
    tipo_usuario = ""
    if tipo_opcion == "1":
        tipo_usuario = "ESTUDIANTE"
    elif tipo_opcion == "2":
        tipo_usuario = "INSTRUCTOR"
    elif tipo_opcion == "3":
        tipo_usuario = "ADMINISTRATIVO"
    else:
        print("\n✗ Opción inválida")
        return False
    
    # Solicitar fecha de préstamo
    fecha_prestamo = input("Fecha de préstamo (YYYY-MM-DD): ").strip()
    if not validar_fecha(fecha_prestamo):
        print("\n✗ Error: Formato de fecha inválido. Use YYYY-MM-DD")
        return False
    
    # Solicitar días solicitados
    try:
        dias_solicitados = int(input("Días solicitados: ").strip())
    except ValueError:
        print("\n✗ Error: Debe ingresar un número válido")
        return False
    
    # Validar límite según tipo de usuario
    dias_maximos = obtener_dias_maximos(tipo_usuario)
    if dias_solicitados > dias_maximos:
        print(f"\n✗ Error: Los {tipo_usuario.lower()}s solo pueden solicitar máximo {dias_maximos} días.")
        print(f"Días solicitados: {dias_solicitados}, Máximo permitido: {dias_maximos}")
        return False
    
    if dias_solicitados <= 0:
        print("\n✗ Error: Los días solicitados deben ser mayor a 0")
        return False
    
    # Generar ID de préstamo
    prestamos = leer_prestamos()
    nuevo_id = len(prestamos) + 1
    prestamo_id = f"P{nuevo_id:04d}"
    
    # Fecha de solicitud (hoy)
    fecha_solicitud = datetime.now().strftime("%Y-%m-%d")
    
    # Extraer mes y año de la fecha de préstamo
    fecha_obj = datetime.strptime(fecha_prestamo, "%Y-%m-%d")
    mes = str(fecha_obj.month).zfill(2)
    anio = str(fecha_obj.year)
    
    # Crear diccionario del préstamo
    nuevo_prestamo = {
        "prestamo_id": prestamo_id,
        "equipo_id": equipo_id,
        "nombre_equipo": equipo.get("nombre_equipo"),
        "usuario_prestatario": usuario_prestatario,
        "tipo_usuario": tipo_usuario,
        "fecha_solicitud": fecha_solicitud,
        "fecha_prestamo": fecha_prestamo,
        "fecha_devolucion": "",
        "dias_autorizados": str(dias_solicitados),
        "dias_reales_usados": "",
        "retraso": "",
        "estado": "PENDIENTE",
        "mes": mes,
        "anio": anio
    }
    
    # Agregar a la lista
    prestamos.append(nuevo_prestamo)
    
    # Guardar
    if guardar_prestamos(prestamos):
        print(f"\n✓ Solicitud de préstamo '{prestamo_id}' registrada exitosamente!")
        print(f"Estado: PENDIENTE - Esperando aprobación")
        return True
    else:
        print("\n✗ Error al registrar la solicitud")
        return False


def listar_prestamos_pendientes():
    """
    Muestra todos los préstamos con estado PENDIENTE
    """
    prestamos = leer_prestamos()
    pendientes = [p for p in prestamos if p.get("estado") == "PENDIENTE"]
    
    if not pendientes:
        print("\nNo hay préstamos pendientes.")
        return []
    
    print("\n" + "="*90)
    print("PRÉSTAMOS PENDIENTES")
    print("="*90)
    print(f"\n{'ID':<10} {'Equipo':<25} {'Usuario':<20} {'Tipo':<15} {'Días':<8} {'Fecha Préstamo':<15}")
    print("-" * 90)
    
    for prestamo in pendientes:
        print(f"{prestamo.get('prestamo_id'):<10} "
              f"{prestamo.get('nombre_equipo'):<25} "
              f"{prestamo.get('usuario_prestatario'):<20} "
              f"{prestamo.get('tipo_usuario'):<15} "
              f"{prestamo.get('dias_autorizados'):<8} "
              f"{prestamo.get('fecha_prestamo'):<15}")
    
    return pendientes


def aprobar_rechazar_prestamo():
    """
    Permite aprobar o rechazar préstamos pendientes
    """
    print("\n" + "="*50)
    print("APROBAR/RECHAZAR PRÉSTAMO")
    print("="*50)
    
    # Listar préstamos pendientes
    pendientes = listar_prestamos_pendientes()
    
    if not pendientes:
        return False
    
    # Solicitar ID del préstamo
    prestamo_id = input("\nIngrese el ID del préstamo a procesar: ").strip()
    
    # Buscar el préstamo
    prestamos = leer_prestamos()
    prestamo_encontrado = None
    indice = -1
    
    for i, prestamo in enumerate(prestamos):
        if prestamo.get("prestamo_id") == prestamo_id:
            if prestamo.get("estado") == "PENDIENTE":
                prestamo_encontrado = prestamo
                indice = i
                break
            else:
                print(f"\n✗ El préstamo '{prestamo_id}' no está pendiente.")
                return False
    
    if not prestamo_encontrado:
        print(f"\n✗ No se encontró un préstamo pendiente con ID '{prestamo_id}'")
        return False
    
    # Mostrar información del préstamo
    print("\n" + "="*50)
    print("INFORMACIÓN DEL PRÉSTAMO")
    print("="*50)
    print(f"ID: {prestamo_encontrado.get('prestamo_id')}")
    print(f"Equipo: {prestamo_encontrado.get('nombre_equipo')}")
    print(f"Usuario: {prestamo_encontrado.get('usuario_prestatario')}")
    print(f"Tipo: {prestamo_encontrado.get('tipo_usuario')}")
    print(f"Días autorizados: {prestamo_encontrado.get('dias_autorizados')}")
    print(f"Fecha préstamo: {prestamo_encontrado.get('fecha_prestamo')}")
    
    # Solicitar decisión
    print("\n¿Qué desea hacer?")
    print("1. Aprobar")
    print("2. Rechazar")
    
    opcion = input("\nSeleccione una opción (1-2): ").strip()
    
    if opcion == "1":
        # Aprobar préstamo
        prestamos[indice]["estado"] = "APROBADO"
        
        # Cambiar estado del equipo a PRESTADO
        equipo_id = prestamo_encontrado.get("equipo_id")
        if equipos.actualizar_estado_equipo(equipo_id, "PRESTADO"):
            if guardar_prestamos(prestamos):
                print(f"\n✓ Préstamo '{prestamo_id}' aprobado exitosamente!")
                print(f"Estado del equipo actualizado a PRESTADO")
                return True
            else:
                print("\n✗ Error al guardar los cambios")
                return False
        else:
            print("\n✗ Error al actualizar el estado del equipo")
            return False
    
    elif opcion == "2":
        # Rechazar préstamo
        prestamos[indice]["estado"] = "RECHAZADO"
        
        if guardar_prestamos(prestamos):
            print(f"\n✓ Préstamo '{prestamo_id}' rechazado.")
            return True
        else:
            print("\n✗ Error al guardar los cambios")
            return False
    
    else:
        print("\n✗ Opción inválida")
        return False


def listar_prestamos_aprobados():
    """
    Muestra todos los préstamos aprobados que aún no han sido devueltos
    """
    prestamos = leer_prestamos()
    aprobados = [p for p in prestamos if p.get("estado") == "APROBADO"]
    
    if not aprobados:
        print("\nNo hay préstamos aprobados sin devolver.")
        return []
    
    print("\n" + "="*90)
    print("PRÉSTAMOS APROBADOS (PENDIENTES DE DEVOLUCIÓN)")
    print("="*90)
    print(f"\n{'ID':<10} {'Equipo':<25} {'Usuario':<20} {'Tipo':<15} {'Días':<8} {'Fecha Préstamo':<15}")
    print("-" * 90)
    
    for prestamo in aprobados:
        print(f"{prestamo.get('prestamo_id'):<10} "
              f"{prestamo.get('nombre_equipo'):<25} "
              f"{prestamo.get('usuario_prestatario'):<20} "
              f"{prestamo.get('tipo_usuario'):<15} "
              f"{prestamo.get('dias_autorizados'):<8} "
              f"{prestamo.get('fecha_prestamo'):<15}")
    
    return aprobados


def registrar_devolucion():
    """
    Permite registrar la devolución de un equipo prestado
    Calcula días reales usados y determina si hubo retraso
    """
    print("\n" + "="*50)
    print("REGISTRAR DEVOLUCIÓN DE EQUIPO")
    print("="*50)
    
    # Listar préstamos aprobados
    aprobados = listar_prestamos_aprobados()
    
    if not aprobados:
        return False
    
    # Solicitar ID del préstamo
    prestamo_id = input("\nIngrese el ID del préstamo a devolver: ").strip()
    
    # Buscar el préstamo
    prestamos = leer_prestamos()
    prestamo_encontrado = None
    indice = -1
    
    for i, prestamo in enumerate(prestamos):
        if prestamo.get("prestamo_id") == prestamo_id:
            if prestamo.get("estado") == "APROBADO":
                prestamo_encontrado = prestamo
                indice = i
                break
            else:
                print(f"\n✗ El préstamo '{prestamo_id}' no está aprobado o ya fue devuelto.")
                return False
    
    if not prestamo_encontrado:
        print(f"\n✗ No se encontró un préstamo aprobado con ID '{prestamo_id}'")
        return False
    
    # Mostrar información
    print("\n" + "="*50)
    print("INFORMACIÓN DEL PRÉSTAMO")
    print("="*50)
    print(f"ID: {prestamo_encontrado.get('prestamo_id')}")
    print(f"Equipo: {prestamo_encontrado.get('nombre_equipo')}")
    print(f"Usuario: {prestamo_encontrado.get('usuario_prestatario')}")
    print(f"Días autorizados: {prestamo_encontrado.get('dias_autorizados')}")
    print(f"Fecha préstamo: {prestamo_encontrado.get('fecha_prestamo')}")
    
    # Solicitar fecha de devolución
    fecha_devolucion = input("\nFecha de devolución (YYYY-MM-DD): ").strip()
    if not validar_fecha(fecha_devolucion):
        print("\n✗ Error: Formato de fecha inválido. Use YYYY-MM-DD")
        return False
    
    # Calcular días reales usados
    fecha_prestamo = prestamo_encontrado.get("fecha_prestamo")
    dias_reales = calcular_dias_diferencia(fecha_prestamo, fecha_devolucion)
    
    if dias_reales < 0:
        print("\n✗ Error: La fecha de devolución no puede ser anterior a la fecha de préstamo")
        return False
    
    # Determinar si hubo retraso
    dias_autorizados = int(prestamo_encontrado.get("dias_autorizados", 0))
    retraso = "SI" if dias_reales > dias_autorizados else "NO"
    
    # Actualizar préstamo
    prestamos[indice]["fecha_devolucion"] = fecha_devolucion
    prestamos[indice]["dias_reales_usados"] = str(dias_reales)
    prestamos[indice]["retraso"] = retraso
    prestamos[indice]["estado"] = "DEVUELTO"
    
    # Cambiar estado del equipo a DISPONIBLE
    equipo_id = prestamo_encontrado.get("equipo_id")
    
    if equipos.actualizar_estado_equipo(equipo_id, "DISPONIBLE"):
        if guardar_prestamos(prestamos):
            print(f"\n✓ Devolución registrada exitosamente!")
            print(f"Días reales usados: {dias_reales}")
            print(f"Días autorizados: {dias_autorizados}")
            if retraso == "SI":
                print(f"⚠ ATENCIÓN: El equipo fue devuelto con retraso de {dias_reales - dias_autorizados} día(s)")
            else:
                print("✓ El equipo fue devuelto a tiempo")
            print(f"Estado del equipo actualizado a DISPONIBLE")
            return True
        else:
            print("\n✗ Error al guardar los cambios")
            return False
    else:
        print("\n✗ Error al actualizar el estado del equipo")
        return False


def consultar_historial():
    """
    Permite consultar el historial de préstamos por equipo o por usuario
    """
    print("\n" + "="*50)
    print("CONSULTAR HISTORIAL DE PRÉSTAMOS")
    print("="*50)
    
    print("\n¿Cómo desea consultar?")
    print("1. Por equipo (ID)")
    print("2. Por usuario")
    
    opcion = input("\nSeleccione una opción (1-2): ").strip()
    
    prestamos = leer_prestamos()
    resultados = []
    
    if opcion == "1":
        equipo_id = input("\nIngrese el ID del equipo: ").strip()
        resultados = [p for p in prestamos if p.get("equipo_id") == equipo_id]
        
    elif opcion == "2":
        usuario = input("\nIngrese el nombre del usuario: ").strip()
        resultados = [p for p in prestamos if p.get("usuario_prestatario") == usuario]
    
    else:
        print("\n✗ Opción inválida")
        return
    
    if not resultados:
        print("\nNo se encontraron préstamos para la búsqueda realizada.")
        return
    
    # Mostrar resultados
    print("\n" + "="*100)
    print("HISTORIAL DE PRÉSTAMOS")
    print("="*100)
    print(f"\n{'ID':<10} {'Equipo':<20} {'Usuario':<20} {'Tipo':<12} {'Estado':<12} {'Días Aut.':<10} {'Días Real':<10} {'Retraso':<8} {'Fecha Prést.':<12} {'Fecha Dev.':<12}")
    print("-" * 100)
    
    for prestamo in resultados:
        fecha_dev = prestamo.get("fecha_devolucion", "N/A")
        dias_real = prestamo.get("dias_reales_usados", "N/A")
        retraso = prestamo.get("retraso", "N/A")
        
        print(f"{prestamo.get('prestamo_id'):<10} "
              f"{prestamo.get('nombre_equipo'):<20} "
              f"{prestamo.get('usuario_prestatario'):<20} "
              f"{prestamo.get('tipo_usuario'):<12} "
              f"{prestamo.get('estado'):<12} "
              f"{prestamo.get('dias_autorizados'):<10} "
              f"{dias_real:<10} "
              f"{retraso:<8} "
              f"{prestamo.get('fecha_prestamo'):<12} "
              f"{fecha_dev:<12}")
    
    print(f"\nTotal de préstamos encontrados: {len(resultados)}")

