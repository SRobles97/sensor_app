# API de Consulta de Sensores

Una API FastAPI para consultar datos de sensores de potencia y discretos almacenados en PostgreSQL.

## Descripción

Este servicio proporciona endpoints RESTful para consultar mediciones de sensores con soporte para rangos de tiempo, paginación optimizada y diferentes tipos de datos de sensores.

## Características

- **Consultas por rango de tiempo**: Filtra datos por fecha y hora específicas
- **Paginación optimizada**: Soporte para cursor-based pagination y paginación tradicional
- **Múltiples tipos de sensores**:
  - Sensores de potencia (mediciones trifásicas eléctricas)
  - Sensores discretos (estados digitales ON/OFF)
- **Pool de conexiones**: Gestión eficiente de conexiones PostgreSQL con asyncpg
- **Documentación automática**: Swagger UI y ReDoc integrados

## Instalación

1. Clona el repositorio:
```bash
git clone <repository-url>
cd sensor_ml_service
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Configura las variables de entorno:
```bash
# Crea un archivo .env con:
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/nombre_db
```

4. Ejecuta el servidor de desarrollo:
```bash
uvicorn app.main:app --reload
```

El servidor estará disponible en `http://localhost:8000`

## Estructura de la Base de Datos

### Tabla: power_measurements
Almacena mediciones eléctricas trifásicas:
- `device`: Identificador del dispositivo
- `timestamp`: Marca temporal de la medición
- Parámetros por fase: corriente, voltaje, potencia activa, potencia aparente, factor de potencia
- Totales del sistema y frecuencia

### Tabla: discrete_measurements  
Almacena estados de sensores digitales:
- `device`: Identificador del dispositivo
- `timestamp`: Marca temporal de la medición
- `d1_state`, `d2_state`, `a1_state`: Estados digitales (ON/OFF)

## Endpoints de la API

### Información del Sistema

#### `GET /`
Devuelve información general del sistema, versión y endpoints disponibles.

### Consultas de Sensores de Potencia

#### `GET /api/power/by-time-range`
Consulta paginada de datos de potencia por rango de tiempo.

**Parámetros:**
- `device` (string): Identificador del dispositivo
- `start_date` (string): Fecha inicial (formato: dd-mm-yyyy)
- `start_time` (string): Hora inicial (formato: HH:MM)
- `end_date` (string): Fecha final (formato: dd-mm-yyyy)
- `end_time` (string): Hora final (formato: HH:MM)
- `page` (int): Número de página (por defecto: 1)
- `page_size` (int): Registros por página (1-1000, por defecto: 500)
- `cursor` (string, opcional): Cursor para paginación optimizada

**Respuesta:**
```json
{
  "data": [...],
  "total_count": 1500,
  "page": 1,
  "page_size": 500,
  "has_next": true,
  "has_previous": false,
  "next_cursor": "2024-01-15T10:30:00"
}
```

#### `GET /api/power/by-time-range/simple`
Consulta simple sin paginación para compatibilidad hacia atrás.

**Parámetros:**
- `device`, `start_date`, `start_time`, `end_date`, `end_time`: Igual que el endpoint anterior
- `limit` (int): Número máximo de registros (1-1000, por defecto: 500)

### Consultas de Sensores Discretos

#### `GET /api/discrete/by-time-range`
Consulta paginada de datos discretos por rango de tiempo.
Mismos parámetros que el endpoint de potencia.

#### `GET /api/discrete/by-time-range/simple`
Consulta simple de datos discretos sin paginación.
Mismos parámetros que el endpoint de potencia simple.

## Ejemplos de Uso

### Consultar datos de potencia
```bash
curl "http://localhost:8000/api/power/by-time-range?device=sensor001&start_date=01-01-2024&start_time=00:00&end_date=01-01-2024&end_time=23:59&page=1&page_size=100"
```

### Consultar datos discretos
```bash
curl "http://localhost:8000/api/discrete/by-time-range/simple?device=sensor002&start_date=15-01-2024&start_time=08:00&end_date=15-01-2024&end_time=18:00&limit=200"
```

## Formatos de Datos

### Datos de Potencia (PowerSensorData)
```json
{
  "device": "sensor001",
  "timestamp": "2024-01-15T10:30:00",
  "i1": 12.5,
  "i2": 11.8,
  "i3": 13.2,
  "v1": 230.1,
  "v2": 229.8,
  "v3": 231.0,
  "p1": 2875.0,
  "p2": 2706.4,
  "p3": 3049.2,
  "pt": 8630.6,
  "frequency": 50.0
}
```

### Datos Discretos (SensorData)
```json
{
  "device": "sensor002",
  "timestamp": "2024-01-15T10:30:00",
  "d1_state": true,
  "d2_state": false,
  "a1_state": true
}
```

## Arquitectura Técnica

- **Framework**: FastAPI con soporte async/await
- **Base de Datos**: PostgreSQL con pool de conexiones asyncpg
- **Modelos**: Pydantic para serialización y validación
- **Estructura modular**: Routers separados para cada tipo de sensor
- **Gestión de errores**: Códigos de estado HTTP y mensajes en español

## Documentación Interactiva

Una vez iniciado el servidor, accede a:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Desarrollo

Para ejecutar en modo desarrollo con recarga automática:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Licencia

[Especificar licencia del proyecto]

## Contribuciones

[Información sobre cómo contribuir al proyecto]