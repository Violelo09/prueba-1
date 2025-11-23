# TechLab Inventory Console – Gestión de equipos tecnológicos

## Datos del Desarrollador

**Proyecto:** Sistema de Gestión de Inventario TechLab  
**Lenguaje:** Python 3  
**Tipo:** Aplicación de consola  
**Fecha:** 2025

---

## Descripción General

El **Sistema de Gestión de Inventario TechLab** es una aplicación de consola desarrollada en Python que permite gestionar el inventario de equipos tecnológicos y controlar los préstamos realizados por estudiantes, instructores y personal administrativo del Laboratorio de Innovación Tecnológica.

El sistema reemplaza el manejo manual en papel o Excel, automatizando:
- El registro y consulta de equipos tecnológicos
- El control de préstamos con validaciones según tipo de usuario
- El cálculo automático de retrasos en devoluciones
- La generación de reportes históricos en formato CSV

---

## Cómo Ejecutar el Programa

### Requisitos Previos

- Python 3.x instalado en el sistema
- Los archivos CSV necesarios en el mismo directorio que el programa

### Pasos para Ejecutar

1. Abrir una terminal o consola en el directorio del proyecto
2. Ejecutar el siguiente comando:

```bash
python main.py
```

3. El sistema solicitará credenciales de inicio de sesión:
   - **Usuario:** admin
   - **Contraseña:** admin123

4. Una vez autenticado, se mostrará el menú principal con las opciones disponibles

### Nota Importante

- El sistema permite máximo **3 intentos** de inicio de sesión
- Si se agotan los intentos, el programa se cerrará automáticamente

---

## Archivos CSV Necesarios

El sistema requiere tres archivos CSV en el mismo directorio:

### 1. usuarios.csv

Archivo que contiene las credenciales del administrador.

**Estructura:**
```
usuario,contrasena,rol
admin,admin123,ADMIN
```

**Campos:**
- `usuario`: Nombre de usuario para login
- `contrasena`: Contraseña del usuario
- `rol`: Rol del usuario (solo ADMIN)

### 2. equipos.csv

Archivo que almacena todos los equipos tecnológicos registrados.

**Estructura:**
```
equipo_id,nombre_equipo,categoria,estado_actual,fecha_registro,descripcion
```

**Campos:**
- `equipo_id`: Identificador único del equipo
- `nombre_equipo`: Nombre descriptivo del equipo (ej: "Laptop Dell XPS")
- `categoria`: Categoría del equipo (drones, laptops, tablets, cámaras, herramientas, etc.)
- `estado_actual`: Estado actual (DISPONIBLE, PRESTADO, MANTENIMIENTO)
- `fecha_registro`: Fecha en que se registró el equipo (formato: YYYY-MM-DD)
- `descripcion`: Descripción opcional del equipo

### 3. prestamos.csv

Archivo que registra todos los préstamos realizados.

**Estructura:**
```
prestamo_id,equipo_id,nombre_equipo,usuario_prestatario,tipo_usuario,fecha_solicitud,fecha_prestamo,fecha_devolucion,dias_autorizados,dias_reales_usados,retraso,estado,mes,anio
```

**Campos:**
- `prestamo_id`: Identificador único del préstamo
- `equipo_id`: ID del equipo prestado
- `nombre_equipo`: Nombre del equipo
- `usuario_prestatario`: Nombre del usuario que solicita el préstamo
- `tipo_usuario`: Tipo de usuario (ESTUDIANTE, INSTRUCTOR, ADMINISTRATIVO)
- `fecha_solicitud`: Fecha en que se realizó la solicitud
- `fecha_prestamo`: Fecha en que se aprobó y entregó el equipo
- `fecha_devolucion`: Fecha en que se devolvió el equipo
- `dias_autorizados`: Días máximos permitidos según tipo de usuario
- `dias_reales_usados`: Días reales que se utilizó el equipo
- `retraso`: Indica si hubo retraso (SI/NO)
- `estado`: Estado del préstamo (PENDIENTE, APROBADO, RECHAZADO, DEVUELTO)
- `mes`: Mes del préstamo (formato: MM)
- `anio`: Año del préstamo (formato: YYYY)

---

## Explicación de las Reglas de Préstamo

### 1. Tiempo Máximo por Tipo de Usuario

Cada tipo de usuario tiene un límite máximo de días para préstamos:

| Tipo de Usuario | Días Máximos |
|----------------|--------------|
| **ESTUDIANTE** | 3 días |
| **INSTRUCTOR** | 7 días |
| **ADMINISTRATIVO** | 10 días |

**Regla:** Si un usuario solicita más días de los permitidos, la solicitud será **rechazada automáticamente**.

### 2. Disponibilidad de Equipos

Un equipo solo puede prestarse si cumple **ambas** condiciones:

1. **Estado DISPONIBLE:** El equipo debe estar marcado como "DISPONIBLE" en el sistema
2. **Sin préstamos pendientes:** No debe tener préstamos con estado "PENDIENTE" o "APROBADO" sin resolver

Si el equipo no está disponible, el sistema **bloqueará el préstamo** y mostrará un mensaje de error.

### 3. Cálculo de Retrasos

Al registrar una devolución, el sistema calcula automáticamente:

- **Días reales usados:** Diferencia entre `fecha_prestamo` y `fecha_devolucion`
- **Retraso:** Se marca como "SI" si `dias_reales_usados > dias_autorizados`

**Ejemplo:**
- Un estudiante tiene autorizados 3 días
- Devuelve el equipo después de 5 días
- Resultado: `retraso = SI` (2 días de retraso)

### 4. Estados de Préstamos

El sistema maneja los siguientes estados:

- **PENDIENTE:** Solicitud registrada, esperando aprobación/rechazo
- **APROBADO:** Préstamo aprobado, equipo entregado
- **RECHAZADO:** Solicitud rechazada por el administrador
- **DEVUELTO:** Equipo devuelto, préstamo completado

### 5. Flujo de Préstamo

1. **Solicitud:** Usuario solicita préstamo → Estado: PENDIENTE
2. **Aprobación/Rechazo:** Administrador decide → Estado: APROBADO o RECHAZADO
3. **Devolución:** Usuario devuelve equipo → Estado: DEVUELTO

---

## Estructura del Proyecto

```
prueba_1/
│
├── main.py              # Punto de entrada, menú principal
├── usuarios.py          # Módulo de autenticación y login
├── equipos.py           # Módulo de gestión de equipos (CRUD)
├── prestamos.py         # Módulo de gestión de préstamos
├── reportes.py          # Módulo de exportación de reportes CSV
│
├── usuarios.csv         # Archivo de usuarios administradores
├── equipos.csv          # Archivo de equipos tecnológicos
├── prestamos.csv        # Archivo de préstamos registrados
│
└── README.md            # Este archivo
```

### Descripción de Módulos

#### main.py
- Punto de entrada del programa
- Maneja el flujo de login y menú principal
- Coordina las llamadas a los demás módulos

#### usuarios.py
- Lectura y validación de credenciales desde `usuarios.csv`
- Función de inicio de sesión con máximo 3 intentos

#### equipos.py
- Funciones CRUD básicas para equipos:
  - `registrar_equipo()`: Registrar nuevo equipo
  - `listar_equipos()`: Mostrar todos los equipos
  - `consultar_equipo()`: Buscar equipo por ID
  - `actualizar_estado_equipo()`: Cambiar estado del equipo

#### prestamos.py
- Gestión completa del ciclo de préstamos:
  - `registrar_solicitud_prestamo()`: Crear nueva solicitud
  - `aprobar_rechazar_prestamo()`: Aprobar o rechazar solicitudes
  - `registrar_devolucion()`: Registrar devolución y calcular retrasos
  - `consultar_historial()`: Consultar historial por equipo o usuario
- Validaciones de límites y disponibilidad

#### reportes.py
- `exportar_reporte_csv()`: Genera reportes CSV filtrados por mes y año
- Solo incluye préstamos DEVUELTOS del período especificado

---

## Limitaciones

1. **Sin base de datos:** Todos los datos se almacenan en archivos CSV, lo que puede ser lento con grandes volúmenes de datos
2. **Un solo administrador:** El sistema solo permite un usuario administrador predefinido
3. **Sin validación de fechas futuras:** El sistema no valida si las fechas de préstamo son futuras
4. **Sin interfaz gráfica:** Es una aplicación exclusivamente de consola
5. **Sin encriptación:** Las contraseñas se almacenan en texto plano en el CSV
6. **Sin historial de cambios:** No se registra quién realizó cada acción
7. **Sin búsqueda avanzada:** Las búsquedas son básicas (por ID o nombre exacto)

---

## Mejoras Futuras

1. **Múltiples usuarios:** Permitir registro de nuevos usuarios con diferentes roles
2. **Validación de fechas:** Validar que las fechas de préstamo no sean futuras
3. **Búsqueda avanzada:** Implementar búsqueda por categoría, estado, rango de fechas
4. **Estadísticas:** Agregar dashboard con estadísticas de préstamos y equipos más prestados
5. **Notificaciones:** Sistema de alertas para préstamos próximos a vencer
6. **Backup automático:** Generar copias de seguridad periódicas de los CSV
7. **Interfaz gráfica:** Migrar a una interfaz gráfica con Tkinter o similar
8. **Base de datos:** Migrar de CSV a SQLite o PostgreSQL para mejor rendimiento
9. **Encriptación:** Implementar hash para contraseñas
10. **Logs de auditoría:** Registrar todas las acciones realizadas en el sistema

---

## Notas Técnicas

- **Python básico:** El código utiliza solo fundamentos de Python (listas, diccionarios, funciones, estructuras de control)
- **Manejo de archivos:** Uso de `open()`, `read()`, `write()` con contexto `with`
- **Sin librerías externas:** No se utilizan librerías como pandas, solo el módulo estándar de Python
- **Formato de fechas:** Todas las fechas usan formato `YYYY-MM-DD`
- **Encoding UTF-8:** Todos los archivos CSV se manejan con encoding UTF-8 para soportar caracteres especiales

---

## Contacto y Soporte

Para consultas o problemas con el sistema, contactar al administrador del TechLab.

---

**Versión:** 1.0  
**Última actualización:** 2025

