"""
Módulo para gestión de equipos tecnológicos
Permite registrar, listar y consultar equipos
"""

from datetime import datetime


def leer_equipos():
    """
    Lee el archivo equipos.csv y retorna una lista de diccionarios
    Cada diccionario representa un equipo con sus datos
    """
    equipos = []
    try:
        with open("equipos.csv", "r", encoding="utf-8") as archivo:
            encabezados = archivo.readline().strip().split(",")
            
            for linea in archivo:
                linea = linea.strip()
                if linea:
                    valores = linea.split(",")
                    equipo = {}
                    for i, encabezado in enumerate(encabezados):
                        equipo[encabezado] = valores[i]
                    equipos.append(equipo)
    except FileNotFoundError:
        print("Error: No se encontró el archivo equipos.csv")
    except Exception as e:
        print(f"Error al leer equipos: {e}")
    
    return equipos


def guardar_equipos(equipos):
    """
    Guarda la lista de equipos en el archivo equipos.csv
    Recibe una lista de diccionarios con los datos de los equipos
    """
    try:
        with open("equipos.csv", "w", encoding="utf-8") as archivo:
            # Escribir encabezados
            encabezados = ["equipo_id", "nombre_equipo", "categoria", "estado_actual", "fecha_registro", "descripcion"]
            archivo.write(",".join(encabezados) + "\n")
            
            # Escribir cada equipo
            for equipo in equipos:
                valores = [
                    equipo.get("equipo_id", ""),
                    equipo.get("nombre_equipo", ""),
                    equipo.get("categoria", ""),
                    equipo.get("estado_actual", ""),
                    equipo.get("fecha_registro", ""),
                    equipo.get("descripcion", "")
                ]
                archivo.write(",".join(valores) + "\n")
        
        return True
    except Exception as e:
        print(f"Error al guardar equipos: {e}")
        return False


def registrar_equipo():
    """
    Permite registrar un nuevo equipo en el sistema
    Solicita los datos necesarios y los guarda en equipos.csv
    """
    print("\n" + "="*50)
    print("REGISTRAR NUEVO EQUIPO")
    print("="*50)
    
    # Leer equipos existentes
    equipos = leer_equipos()
    
    # Solicitar datos del equipo
    equipo_id = input("\nID del equipo: ").strip()
    
    # Validar que el ID no exista
    for equipo in equipos:
        if equipo.get("equipo_id") == equipo_id:
            print(f"\n✗ Error: Ya existe un equipo con ID '{equipo_id}'")
            return False
    
    nombre_equipo = input("Nombre del equipo: ").strip()
    categoria = input("Categoría (drones, laptops, tablets, cámaras, herramientas, etc.): ").strip()
    
    # Estado por defecto es DISPONIBLE
    estado_actual = "DISPONIBLE"
    
    # Fecha de registro (fecha actual)
    fecha_registro = datetime.now().strftime("%Y-%m-%d")
    
    descripcion = input("Descripción (opcional, presiona Enter para omitir): ").strip()
    
    # Crear diccionario con los datos del equipo
    nuevo_equipo = {
        "equipo_id": equipo_id,
        "nombre_equipo": nombre_equipo,
        "categoria": categoria,
        "estado_actual": estado_actual,
        "fecha_registro": fecha_registro,
        "descripcion": descripcion
    }
    
    # Agregar a la lista
    equipos.append(nuevo_equipo)
    
    # Guardar en el archivo
    if guardar_equipos(equipos):
        print(f"\n✓ Equipo '{nombre_equipo}' registrado exitosamente!")
        return True
    else:
        print("\n✗ Error al registrar el equipo")
        return False


def listar_equipos():
    """
    Muestra todos los equipos registrados en formato de tabla
    """
    print("\n" + "="*80)
    print("LISTADO DE EQUIPOS")
    print("="*80)
    
    equipos = leer_equipos()
    
    if not equipos:
        print("\nNo hay equipos registrados.")
        return
    
    # Mostrar encabezados
    print(f"\n{'ID':<15} {'Nombre':<30} {'Categoría':<20} {'Estado':<15}")
    print("-" * 80)
    
    # Mostrar cada equipo
    for equipo in equipos:
        equipo_id = equipo.get("equipo_id", "")
        nombre = equipo.get("nombre_equipo", "")
        categoria = equipo.get("categoria", "")
        estado = equipo.get("estado_actual", "")
        
        print(f"{equipo_id:<15} {nombre:<30} {categoria:<20} {estado:<15}")
    
    print(f"\nTotal de equipos: {len(equipos)}")


def consultar_equipo():
    """
    Permite buscar y mostrar la información completa de un equipo por su ID
    """
    print("\n" + "="*50)
    print("CONSULTAR EQUIPO")
    print("="*50)
    
    equipo_id = input("\nIngrese el ID del equipo a consultar: ").strip()
    
    equipos = leer_equipos()
    
    # Buscar el equipo
    equipo_encontrado = None
    for equipo in equipos:
        if equipo.get("equipo_id") == equipo_id:
            equipo_encontrado = equipo
            break
    
    if equipo_encontrado:
        print("\n" + "="*50)
        print("INFORMACIÓN DEL EQUIPO")
        print("="*50)
        print(f"\nID: {equipo_encontrado.get('equipo_id')}")
        print(f"Nombre: {equipo_encontrado.get('nombre_equipo')}")
        print(f"Categoría: {equipo_encontrado.get('categoria')}")
        print(f"Estado: {equipo_encontrado.get('estado_actual')}")
        print(f"Fecha de registro: {equipo_encontrado.get('fecha_registro')}")
        descripcion = equipo_encontrado.get('descripcion', '')
        if descripcion:
            print(f"Descripción: {descripcion}")
        else:
            print("Descripción: (sin descripción)")
    else:
        print(f"\n✗ No se encontró un equipo con ID '{equipo_id}'")


def obtener_equipo_por_id(equipo_id):
    """
    Función auxiliar para obtener un equipo por su ID
    Retorna el diccionario del equipo si existe, None si no existe
    """
    equipos = leer_equipos()
    for equipo in equipos:
        if equipo.get("equipo_id") == equipo_id:
            return equipo
    return None


def actualizar_estado_equipo(equipo_id, nuevo_estado):
    """
    Actualiza el estado de un equipo en el archivo CSV
    Recibe el ID del equipo y el nuevo estado
    Retorna True si se actualizó correctamente, False en caso contrario
    """
    equipos = leer_equipos()
    
    # Buscar y actualizar el equipo
    encontrado = False
    for equipo in equipos:
        if equipo.get("equipo_id") == equipo_id:
            equipo["estado_actual"] = nuevo_estado
            encontrado = True
            break
    
    if encontrado:
        return guardar_equipos(equipos)
    else:
        return False

