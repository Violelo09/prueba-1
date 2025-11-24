from datetime import datetime  # para obtener la fecha actual

# =========================================================
# FUNCIÓN: leer_equipos()
# Lee el archivo equipos.csv y devuelve una lista de diccionarios,
# donde cada diccionario es un equipo con todos sus datos.
# =========================================================
def leer_equipos():
    equipos = []  # lista donde guardaremos todos los equipos
    
    try:
        # Abrimos el archivo en modo lectura
        with open("equipos.csv", "r", encoding="utf-8") as archivo:
            
            # Leer la primera línea (los encabezados)
            encabezados = archivo.readline().strip().split(",")
            
            # Leer cada línea restante del archivo
            for linea in archivo:
                linea = linea.strip()  # quitar espacios y saltos de línea
                
                if linea:  # si la línea no está vacía
                    valores = linea.split(",")  # separar por comas
                    
                    equipo = {}  # aquí guardaremos un equipo
                    
                    # Construimos el diccionario: encabezado → valor
                    for i, encabezado in enumerate(encabezados):
                        equipo[encabezado] = valores[i]
                    
                    equipos.append(equipo)  # agregar a la lista
    
    except FileNotFoundError:
        print("Error: No se encontró el archivo equipos.csv")
    
    except Exception as e:
        print(f"Error al leer equipos: {e}")
    
    return equipos  # lista de diccionarios

# =========================================================
# FUNCIÓN: guardar_equipos()
# Guarda todos los equipos en el archivo CSV.
# Sobrescribe el archivo con los datos nuevos.
# =========================================================
def guardar_equipos(equipos):
    try:
        with open("equipos.csv", "w", encoding="utf-8") as archivo:
            
            # Encabezados que queremos escribir
            encabezados = ["equipo_id", "nombre_equipo", "categoria", "estado_actual", "fecha_registro", "descripcion"]
            
            archivo.write(",".join(encabezados) + "\n")  # escribir encabezados
            
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
                
                archivo.write(",".join(valores) + "\n")  # escribir fila
        
        return True
    
    except Exception as e:
        print(f"Error al guardar equipos: {e}")
        return False

# =========================================================
# FUNCIÓN: registrar_equipo()
# Pide los datos del usuario, crea un nuevo equipo y lo guarda.
# =========================================================
def registrar_equipo():
    print("\n" + "="*50)
    print("REGISTRAR NUEVO EQUIPO")
    print("="*50)
    
    equipos = leer_equipos()  # cargar equipos existentes
    
    # Pedir ID del equipo
    equipo_id = input("\nID del equipo: ").strip()
    
    # Validar que NO exista ese ID
    for equipo in equipos:
        if equipo.get("equipo_id") == equipo_id:
            print(f"\n✗ Error: Ya existe un equipo con ID '{equipo_id}'")
            return False
    
    # Pedir más datos
    nombre_equipo = input("Nombre del equipo: ").strip()
    categoria = input("Categoría (drones, laptops, etc.): ").strip()
    
    estado_actual = "DISPONIBLE"  # estado por defecto
    
    fecha_registro = datetime.now().strftime("%Y-%m-%d")  # fecha actual
    
    descripcion = input("Descripción (opcional): ").strip()
    
    # Crear el diccionario del equipo
    nuevo_equipo = {
        "equipo_id": equipo_id,
        "nombre_equipo": nombre_equipo,
        "categoria": categoria,
        "estado_actual": estado_actual,
        "fecha_registro": fecha_registro,
        "descripcion": descripcion
    }
    
    equipos.append(nuevo_equipo)  # agregar a la lista
    
    # Guardar en el archivo
    if guardar_equipos(equipos):
        print(f"\n✓ Equipo '{nombre_equipo}' registrado exitosamente!")
        return True
    else:
        print("\n✗ Error al registrar el equipo")
        return False

# =========================================================
# FUNCIÓN: listar_equipos()
# Muestra todos los equipos en forma de tabla.
# =========================================================
def listar_equipos():
    print("\n" + "="*80)
    print("LISTADO DE EQUIPOS")
    print("="*80)
    
    equipos = leer_equipos()  # cargar equipos
    
    if not equipos:  # si está vacío
        print("\nNo hay equipos registrados.")
        return
    
    # Encabezados de la tabla
    print(f"\n{'ID':<15} {'Nombre':<30} {'Categoría':<20} {'Estado':<15}")
    print("-" * 80)
    
    # Mostrar cada equipo
    for equipo in equipos:
        print(f"{equipo.get('equipo_id',''):<15} "
              f"{equipo.get('nombre_equipo',''):<30} "
              f"{equipo.get('categoria',''):<20} "
              f"{equipo.get('estado_actual',''):<15}")
    
    print(f"\nTotal de equipos: {len(equipos)}")

# =========================================================
# FUNCIÓN: consultar_equipo()
# Busca un equipo por su ID y muestra toda su información.
# =========================================================
def consultar_equipo():
    print("\n" + "="*50)
    print("CONSULTAR EQUIPO")
    print("="*50)
    
    equipo_id = input("\nIngrese el ID del equipo a consultar: ").strip()
    
    equipos = leer_equipos()
    
    equipo_encontrado = None  # por si se encuentra
    
    # Buscar el equipo
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

# =========================================================
# FUNCIÓN: obtener_equipo_por_id()
# Devuelve un equipo por ID o None si no existe.
# =========================================================
def obtener_equipo_por_id(equipo_id):
    equipos = leer_equipos()
    
    for equipo in equipos:
        if equipo.get("equipo_id") == equipo_id:
            return equipo  # lo encontró
    
    return None  # no existe

# =========================================================
# FUNCIÓN: actualizar_estado_equipo()
# Cambia el estado de un equipo en el CSV.
# =========================================================
def actualizar_estado_equipo(equipo_id, nuevo_estado):
    equipos = leer_equipos()
    
    encontrado = False  # bandera
    
    for equipo in equipos:
        if equipo.get("equipo_id") == equipo_id:
            equipo["estado_actual"] = nuevo_estado
            encontrado = True
            break
    
    if encontrado:
        return guardar_equipos(equipos)  # guardar cambios
    else:
        return False  # no se encontró ese Informe 
