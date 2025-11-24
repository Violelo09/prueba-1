"""
Módulo para gestión de préstamos de equipos
Maneja solicitudes, aprobaciones, rechazos y devoluciones
"""
rom datetime import datetime, timedelta
import equipos

# =========================================================
# prestamos_comentado.py
# Versión del módulo 'prestamos' con comentarios claros y
# sencillos en español para estudiar.
# =========================================================

def leer_prestamos():
    """
    Lee prestamos.csv y devuelve una lista de diccionarios.
    Cada diccionario representa un préstamo.
    """
    prestamos = []  # lista donde guardamos los préstamos
    try:
        with open("prestamos.csv", "r", encoding="utf-8") as archivo:
            # La primera línea se asume que son los encabezados
            encabezados = archivo.readline().strip().split(",")

            # Recorrer cada línea del archivo (cada préstamo)
            for linea in archivo:
                linea = linea.strip()
                if linea:  # si la línea no está vacía
                    valores = linea.split(",")  # separar por comas
                    prestamo = {}
                    # Construir el diccionario: encabezado -> valor correspondiente
                    for i, encabezado in enumerate(encabezados):
                        prestamo[encabezado] = valores[i]
                    prestamos.append(prestamo)  # añadir a la lista
    except FileNotFoundError:
        # Si no existe el archivo, avisamos y devolvemos lista vacía
        print("Error: No se encontró el archivo prestamos.csv")
    except Exception as e:
        # Cualquier otro error lo mostramos (útil para depurar)
        print(f"Error al leer préstamos: {e}")

    return prestamos

def guardar_prestamos(prestamos):
    """
    Guarda la lista completa de préstamos en prestamos.csv.
    Sobrescribe el archivo con los datos actuales.
    """
    try:
        with open("prestamos.csv", "w", encoding="utf-8") as archivo:
            # Definimos los encabezados que queremos en el CSV
            encabezados = [
                "prestamo_id", "equipo_id", "nombre_equipo", "usuario_prestatario",
                "tipo_usuario", "fecha_solicitud", "fecha_prestamo", "fecha_devolucion",
                "dias_autorizados", "dias_reales_usados", "retraso", "estado", "mes", "anio"
            ]
            archivo.write(",".join(encabezados) + "\n")  # escribir primera línea

            # Escribir cada préstamo en una línea del CSV
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
        # Si ocurre un error al escribir, mostrar y devolver False
        print(f"Error al guardar préstamos: {e}")
        return False

def obtener_dias_maximos(tipo_usuario):
    """
    Devuelve la cantidad máxima de días permitidos según tipo de usuario.
    - ESTUDIANTE: 3 días
    - INSTRUCTOR: 7 días
    - ADMINISTRATIVO: 10 días
    Si no reconoce el tipo devuelve 0.
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
    Verifica que la cadena fecha_str tenga formato 'YYYY-MM-DD'.
    Devuelve True si es válida, False si no.
    """
    try:
        datetime.strptime(fecha_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def calcular_dias_diferencia(fecha_inicio, fecha_fin):
    """
    Calcula cuántos días hay entre fecha_inicio y fecha_fin.
    Ambas en formato 'YYYY-MM-DD'. Devuelve un entero (días).
    Si las fechas no son válidas devuelve 0.
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
    Permite crear una nueva solicitud de préstamo:
    - Muestra equipos DISPONIBLES
    - Pide datos del usuario y del préstamo
    - Valida que el equipo exista, esté disponible y no tenga préstamos pendientes
    - Valida el tipo de usuario y los días solicitados
    - Guarda la solicitud en prestamos.csv con estado 'PENDIENTE'
    """
    print("\n" + "="*50)
    print("REGISTRAR SOLICITUD DE PRÉSTAMO")
    print("="*50)

    # Mostrar equipos disponibles para elegir
    print("\nEquipos disponibles:")
    equipos_lista = equipos.leer_equipos()  # leer equipos desde equipos.py
    disponibles = [e for e in equipos_lista if e.get("estado_actual") == "DISPONIBLE"]

    if not disponibles:
        # Si no hay ningún equipo DISPONIBLE, salimos
        print("\n✗ No hay equipos disponibles en este momento.")
        return False

    # Mostrar una tabla simple con ID, nombre y categoría
    print(f"\n{'ID':<15} {'Nombre':<30} {'Categoría':<20}")
    print("-" * 65)
    for equipo in disponibles:
        print(f"{equipo.get('equipo_id'):<15} {equipo.get('nombre_equipo'):<30} {equipo.get('categoria'):<20}")

    # -----------------------------
    # Pedir ID del equipo a prestar
    # -----------------------------
    equipo_id = input("\nIngrese el ID del equipo a prestar: ").strip()

    # Validar que existe el equipo y que está disponible
    equipo = equipos.obtener_equipo_por_id(equipo_id)
    if not equipo:
        print(f"\n✗ Error: No se encontró un equipo con ID '{equipo_id}'")
        return False

    if equipo.get("estado_actual") != "DISPONIBLE":
        print(f"\n✗ Error: El equipo '{equipo.get('nombre_equipo')}' no está disponible.")
        print(f"Estado actual: {equipo.get('estado_actual')}")
        return False

    # -----------------------------
    # Verificar que no tenga préstamos pendientes
    # -----------------------------
    prestamos = leer_prestamos()
    for prestamo in prestamos:
        if (prestamo.get("equipo_id") == equipo_id and 
            prestamo.get("estado") in ["PENDIENTE", "APROBADO"]):
            # Si hay un préstamo pendiente o aprobado, no se puede solicitar otro
            print(f"\n✗ Error: El equipo tiene un préstamo {prestamo.get('estado').lower()} sin resolver.")
            return False

    # -----------------------------
    # Datos del prestatario
    # -----------------------------
    usuario_prestatario = input("Nombre del usuario prestatario: ").strip()

    # Mostrar opciones de tipo de usuario con explicación de días máximos
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
        # Opción inválida -> salir
        print("\n✗ Opción inválida")
        return False

    # -----------------------------
    # Fecha de préstamo (debe tener formato correcto)
    # -----------------------------
    fecha_prestamo = input("Fecha de préstamo (YYYY-MM-DD): ").strip()
    if not validar_fecha(fecha_prestamo):
        print("\n✗ Error: Formato de fecha inválido. Use YYYY-MM-DD")
        return False

    # -----------------------------
    # Días solicitados (número entero)
    # -----------------------------
    try:
        dias_solicitados = int(input("Días solicitados: ").strip())
    except ValueError:
        print("\n✗ Error: Debe ingresar un número válido")
        return False

    # Validar que los días solicitados no superen el máximo según tipo de usuario
    dias_maximos = obtener_dias_maximos(tipo_usuario)
    if dias_solicitados > dias_maximos:
        print(f"\n✗ Error: Los {tipo_usuario.lower()}s solo pueden solicitar máximo {dias_maximos} días.")
        print(f"Días solicitados: {dias_solicitados}, Máximo permitido: {dias_maximos}")
        return False

    # Validar que pida al menos 1 día
    if dias_solicitados <= 0:
        print("\n✗ Error: Los días solicitados deben ser mayor a 0")
        return False

    # -----------------------------
    # Generar ID de préstamo y otros campos
    # -----------------------------
    prestamos = leer_prestamos()
    nuevo_id = len(prestamos) + 1  # simple: número siguiente
    prestamo_id = f"P{nuevo_id:04d}"  # formato P0001, P0002, ...

    fecha_solicitud = datetime.now().strftime("%Y-%m-%d")  # fecha de hoy

    # Extraer mes y año de la fecha de préstamo (útil para reportes)
    fecha_obj = datetime.strptime(fecha_prestamo, "%Y-%m-%d")
    mes = str(fecha_obj.month).zfill(2)
    anio = str(fecha_obj.year)

    # Crear diccionario con toda la info del préstamo
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
        "estado": "PENDIENTE",  # inicialmente pendiente de aprobación
        "mes": mes,
        "anio": anio
    }

    # Añadir y guardar
    prestamos.append(nuevo_prestamo)

    if guardar_prestamos(prestamos):
        print(f"\n✓ Solicitud de préstamo '{prestamo_id}' registrada exitosamente!")
        print(f"Estado: PENDIENTE - Esperando aprobación")
        return True
    else:
        print("\n✗ Error al registrar la solicitud")
        return False


def listar_prestamos_pendientes():
    """
    Devuelve y muestra los préstamos con estado PENDIENTE.
    """
    prestamos = leer_prestamos()
    pendientes = [p for p in prestamos if p.get("estado") == "PENDIENTE"]

    if not pendientes:
        print("\nNo hay préstamos pendientes.")
        return []

    # Mostrar tabla de pendientes
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
    Permite al encargado aprobar o rechazar préstamos que estén PENDIENTES.
    - Si aprueba, cambia el estado del préstamo a APROBADO y del equipo a PRESTADO.
    - Si rechaza, cambia el estado a RECHAZADO.
    """
    print("\n" + "="*50)
    print("APROBAR/RECHAZAR PRÉSTAMO")
    print("="*50)

    # Mostrar pendientes y pedir elegir uno
    pendientes = listar_prestamos_pendientes()

    if not pendientes:
        return False

    prestamo_id = input("\nIngrese el ID del préstamo a procesar: ").strip()

    prestamos = leer_prestamos()
    prestamo_encontrado = None
    indice = -1

    # Buscar el préstamo por ID y comprobar que esté PENDIENTE
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

    # Mostrar información básica del préstamo
    print("\n" + "="*50)
    print("INFORMACIÓN DEL PRÉSTAMO")
    print("="*50)
    print(f"ID: {prestamo_encontrado.get('prestamo_id')}")
    print(f"Equipo: {prestamo_encontrado.get('nombre_equipo')}")
    print(f"Usuario: {prestamo_encontrado.get('usuario_prestatario')}")
    print(f"Tipo: {prestamo_encontrado.get('tipo_usuario')}")
    print(f"Días autorizados: {prestamo_encontrado.get('dias_autorizados')}")
    print(f"Fecha préstamo: {prestamo_encontrado.get('fecha_prestamo')}")

    # Decisión del encargado
    print("\n¿Qué desea hacer?")
    print("1. Aprobar")
    print("2. Rechazar")

    opcion = input("\nSeleccione una opción (1-2): ").strip()

    if opcion == "1":
        # Si aprueba, actualizar el estado del préstamo
        prestamos[indice]["estado"] = "APROBADO"

        # Actualizar el estado del equipo a PRESTADO (usa equipos.actualizar_estado_equipo)
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
        # Si rechaza, solo actualizamos el estado a RECHAZADO
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
    Muestra préstamos aprobados y que aún no han sido devueltos (estado APROBADO).
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
    Registra la devolución de un préstamo aprobado:
    - Pide fecha de devolución
    - Calcula días reales usados y si hubo retraso
    - Actualiza el préstamo y pone el equipo como DISPONIBLE
    """
    print("\n" + "="*50)
    print("REGISTRAR DEVOLUCIÓN DE EQUIPO")
    print("="*50)

    aprobados = listar_prestamos_aprobados()

    if not aprobados:
        return False

    prestamo_id = input("\nIngrese el ID del préstamo a devolver: ").strip()

    prestamos = leer_prestamos()
    prestamo_encontrado = None
    indice = -1

    # Buscar el préstamo y comprobar que está APROBADO
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

    # Mostrar datos importantes antes de devolver
    print("\n" + "="*50)
    print("INFORMACIÓN DEL PRÉSTAMO")
    print("="*50)
    print(f"ID: {prestamo_encontrado.get('prestamo_id')}")
    print(f"Equipo: {prestamo_encontrado.get('nombre_equipo')}")
    print(f"Usuario: {prestamo_encontrado.get('usuario_prestatario')}")
    print(f"Días autorizados: {prestamo_encontrado.get('dias_autorizados')}")
    print(f"Fecha préstamo: {prestamo_encontrado.get('fecha_prestamo')}")

    # Pedir la fecha real de devolución
    fecha_devolucion = input("\nFecha de devolución (YYYY-MM-DD): ").strip()
    if not validar_fecha(fecha_devolucion):
        print("\n✗ Error: Formato de fecha inválido. Use YYYY-MM-DD")
        return False

    # Calcular días reales usados (puede ser 0 o más)
    fecha_prestamo = prestamo_encontrado.get("fecha_prestamo")
    dias_reales = calcular_dias_diferencia(fecha_prestamo, fecha_devolucion)

    if dias_reales < 0:
        # No se permite devolver antes de la fecha de préstamo
        print("\n✗ Error: La fecha de devolución no puede ser anterior a la fecha de préstamo")
        return False

    # Comprobar si hubo retraso comparando días reales con días autorizados
    dias_autorizados = int(prestamo_encontrado.get("dias_autorizados", 0))
    retraso = "SI" if dias_reales > dias_autorizados else "NO"

    # Actualizar campos del préstamo
    prestamos[indice]["fecha_devolucion"] = fecha_devolucion
    prestamos[indice]["dias_reales_usados"] = str(dias_reales)
    prestamos[indice]["retraso"] = retraso
    prestamos[indice]["estado"] = "DEVUELTO"

    # Cambiar el estado del equipo a DISPONIBLE
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
    Permite buscar préstamos por equipo (ID) o por usuario.
    Muestra una tabla con los resultados y el total encontrado.
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

    # Mostrar encabezados y cada registro encontrado
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
