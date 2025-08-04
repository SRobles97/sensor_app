from pydantic import BaseModel
from datetime import datetime


class SensorData(BaseModel):
    """
    Modelo de respuesta para datos de sensores discretos/digitales.

    Este modelo representa la estructura de datos que se retorna en las respuestas
    de los endpoints que consultan mediciones de entradas discretas. Se utiliza
    principalmente para serialización JSON en las respuestas de la API.

    Casos de uso:
    - Respuestas del endpoint GET /discrete_measurements
    - Serialización de datos para dashboards y visualizaciones
    - Integración con sistemas de monitoreo de estados digitales
    - APIs de consulta de históricos de sensores ON/OFF

    Estructura de respuesta JSON:
    {
        "device": "sensor001",
        "timestamp": "2025-01-15T10:30:00.000Z",
        "d1_state": 1,
        "d2_state": 0,
        "a1_state": 1
    }
    """

    # Identificador único del dispositivo sensor
    device: str

    # Marca de tiempo de la medición (se serializa automáticamente a ISO format)
    timestamp: datetime

    # Estado de la entrada digital 1 (0=OFF, 1=ON)
    d1_state: int

    # Estado de la entrada digital 2 (0=OFF, 1=ON)
    d2_state: int

    # Estado de la entrada analógica 1 convertida a digital (0=OFF, 1=ON)
    a1_state: int

    class Config:
        """
        Configuración del modelo para serialización JSON.

        json_encoders define cómo se deben serializar tipos específicos:
        - datetime: Se convierte automáticamente a formato ISO 8601
        """

        json_encoders = {datetime: lambda v: v.isoformat()}
