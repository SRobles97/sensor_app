from datetime import datetime
from pydantic import BaseModel


class PowerSensorData(BaseModel):
    """
    Modelo de respuesta para datos de sensores de energía trifásicos.

    Este modelo representa la estructura completa de datos energéticos que se retorna
    en las respuestas de los endpoints que consultan mediciones de potencia. Incluye
    todos los parámetros eléctricos de las tres fases más los totales del sistema.

    Casos de uso:
    - Respuestas del endpoint GET /power_measurements
    - APIs de consulta de históricos energéticos
    - Dashboards de monitoreo energético en tiempo real
    - Sistemas SCADA y de gestión energética
    - Análisis de calidad de energía y eficiencia
    - Reportes de consumo y facturación energética

    Estructura de respuesta JSON:
    {
        "device": "medidor001",
        "timestamp": "2025-01-15T10:30:00.000Z",
        "phase_a_current": 15.2,
        "phase_a_voltage": 220.5,
        ...
        "total_active_power": 10028.0
    }
    """

    # Identificador único del medidor energético
    device: str

    # Marca de tiempo de la medición energética
    timestamp: datetime

    # === PARÁMETROS ELÉCTRICOS FASE A ===
    phase_a_current: float  # Corriente fase A en Amperios (A)
    phase_a_voltage: float  # Voltaje fase A en Voltios (V)
    phase_a_active_power: float  # Potencia activa fase A en Watts (W)
    phase_a_apparent_power: float  # Potencia aparente fase A en Volt-Amperios (VA)
    phase_a_power_factor: float  # Factor de potencia fase A (0.0 - 1.0)
    phase_a_frequency: float  # Frecuencia fase A en Hertz (Hz)

    # === PARÁMETROS ELÉCTRICOS FASE B ===
    phase_b_current: float  # Corriente fase B en Amperios (A)
    phase_b_voltage: float  # Voltaje fase B en Voltios (V)
    phase_b_active_power: float  # Potencia activa fase B en Watts (W)
    phase_b_apparent_power: float  # Potencia aparente fase B en Volt-Amperios (VA)
    phase_b_power_factor: float  # Factor de potencia fase B (0.0 - 1.0)
    phase_b_frequency: float  # Frecuencia fase B en Hertz (Hz)

    # === PARÁMETROS ELÉCTRICOS FASE C ===
    phase_c_current: float  # Corriente fase C en Amperios (A)
    phase_c_voltage: float  # Voltaje fase C en Voltios (V)
    phase_c_active_power: float  # Potencia activa fase C en Watts (W)
    phase_c_apparent_power: float  # Potencia aparente fase C en Volt-Amperios (VA)
    phase_c_power_factor: float  # Factor de potencia fase C (0.0 - 1.0)
    phase_c_frequency: float  # Frecuencia fase C en Hertz (Hz)

    # === TOTALES DEL SISTEMA TRIFÁSICO ===
    total_current: float  # Corriente total del sistema en Amperios (A)
    total_active_power: float  # Potencia activa total en Watts (W)
    total_apparent_power: float  # Potencia aparente total en Volt-Amperios (VA)

    class Config:
        """
        Configuración del modelo para serialización JSON.

        json_encoders personaliza la serialización de tipos específicos:
        - datetime: Automáticamente convertido a formato ISO 8601 (YYYY-MM-DDTHH:MM:SS.sssZ)

        Esto garantiza que las fechas sean consistentes y parseables por
        clientes JavaScript, sistemas de monitoreo y herramientas de análisis.
        """

        json_encoders = {datetime: lambda v: v.isoformat()}
