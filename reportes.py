"""
Módulo para generar reportes en formato CSV
Exporta reportes de préstamos por mes y año
"""


def leer_prestamos():
    """
    Lee el archivo prestamos.csv y retorna una lista de diccionarios
    Función auxiliar para evitar importar prestamos.py (evitar dependencias circulares)
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


def exportar_reporte_csv():
    """
    Permite exportar un reporte CSV de préstamos devueltos por mes y año
    Solo incluye préstamos con estado DEVUELTO del mes y año especificados
    """
    print("\n" + "="*50)
    print("EXPORTAR REPORTE CSV")
    print("="*50)
    
    # Solicitar mes y año
    try:
        anio = input("\nIngrese el año (ej: 2025): ").strip()
        mes = input("Ingrese el mes (1-12): ").strip()
        
        # Validar mes
        mes_num = int(mes)
        if mes_num < 1 or mes_num > 12:
            print("\n✗ Error: El mes debe estar entre 1 y 12")
            return False
        
        # Formatear mes con dos dígitos
        mes_formateado = str(mes_num).zfill(2)
        
    except ValueError:
        print("\n✗ Error: Debe ingresar números válidos")
        return False
    
    # Leer préstamos
    prestamos = leer_prestamos()
    
    # Filtrar préstamos devueltos del mes y año especificados
    prestamos_filtrados = []
    for prestamo in prestamos:
        if (prestamo.get("estado") == "DEVUELTO" and
            prestamo.get("anio") == anio and
            prestamo.get("mes") == mes_formateado):
            prestamos_filtrados.append(prestamo)
    
    # Verificar si hay datos
    if not prestamos_filtrados:
        print(f"\n✗ No hay préstamos devueltos para el mes {mes_formateado} del año {anio}")
        return False
    
    # Generar nombre del archivo
    nombre_archivo = f"reporte_prestamos_{anio}_{mes_formateado}.csv"
    
    try:
        # Crear y escribir el archivo CSV
        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            # Escribir encabezados
            encabezados = [
                "prestamo_id", "equipo_id", "nombre_equipo", "usuario_prestatario",
                "tipo_usuario", "dias_autorizados", "dias_reales_usados", "retraso",
                "estado", "mes", "anio"
            ]
            archivo.write(",".join(encabezados) + "\n")
            
            # Escribir cada préstamo filtrado
            for prestamo in prestamos_filtrados:
                valores = [
                    prestamo.get("prestamo_id", ""),
                    prestamo.get("equipo_id", ""),
                    prestamo.get("nombre_equipo", ""),
                    prestamo.get("usuario_prestatario", ""),
                    prestamo.get("tipo_usuario", ""),
                    prestamo.get("dias_autorizados", ""),
                    prestamo.get("dias_reales_usados", ""),
                    prestamo.get("retraso", ""),
                    prestamo.get("estado", ""),
                    prestamo.get("mes", ""),
                    prestamo.get("anio", "")
                ]
                archivo.write(",".join(valores) + "\n")
        
        print(f"\n✓ Reporte exportado exitosamente!")
        print(f"Archivo generado: {nombre_archivo}")
        print(f"Total de préstamos incluidos: {len(prestamos_filtrados)}")
        return True
        
    except Exception as e:
        print(f"\n✗ Error al generar el reporte: {e}")
        return False

