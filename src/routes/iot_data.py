import random
from datetime import datetime, timedelta
from flask import Blueprint, jsonify
import json
import os
from flask_cors import cross_origin

iot_data_bp = Blueprint("iot_data", __name__)

# Datos simulados en memoria para evitar dependencias externas
# SIMULATED_DATA = [
#     {"timestamp": "2025-08-30T00:00:00", "temperatura_celsius": 38.2, "frecuencia_cardiaca_lpm": 95},
#     {"timestamp": "2025-08-30T00:05:00", "temperatura_celsius": 38.1, "frecuencia_cardiaca_lpm": 92},
#     {"timestamp": "2025-08-30T00:10:00", "temperatura_celsius": 38.3, "frecuencia_cardiaca_lpm": 98},
#     {"timestamp": "2025-08-30T00:15:00", "temperatura_celsius": 38.0, "frecuencia_cardiaca_lpm": 89},
#     {"timestamp": "2025-08-30T00:20:00", "temperatura_celsius": 38.4, "frecuencia_cardiaca_lpm": 101},
#     {"timestamp": "2025-08-30T06:00:00", "temperatura_celsius": 39.8, "frecuencia_cardiaca_lpm": 105},  # Fiebre
#     {"timestamp": "2025-08-30T06:05:00", "temperatura_celsius": 40.2, "frecuencia_cardiaca_lpm": 108},  # Fiebre
#     {"timestamp": "2025-08-30T06:10:00", "temperatura_celsius": 40.0, "frecuencia_cardiaca_lpm": 110},  # Fiebre
#     {"timestamp": "2025-08-30T14:00:00", "temperatura_celsius": 38.5, "frecuencia_cardiaca_lpm": 135},  # Taquicardia
#     {"timestamp": "2025-08-30T14:05:00", "temperatura_celsius": 38.3, "frecuencia_cardiaca_lpm": 142},  # Taquicardia
#     {"timestamp": "2025-08-30T14:10:00", "temperatura_celsius": 38.4, "frecuencia_cardiaca_lpm": 138},  # Taquicardia
#     {"timestamp": "2025-08-30T20:00:00", "temperatura_celsius": 40.5, "frecuencia_cardiaca_lpm": 155},  # Fiebre + Taquicardia
#     {"timestamp": "2025-08-30T20:05:00", "temperatura_celsius": 40.8, "frecuencia_cardiaca_lpm": 162},  # Fiebre + Taquicardia
#     {"timestamp": "2025-08-30T20:10:00", "temperatura_celsius": 40.3, "frecuencia_cardiaca_lpm": 158},  # Fiebre + Taquicardia
#     {"timestamp": "2025-08-30T23:55:00", "temperatura_celsius": 38.6, "frecuencia_cardiaca_lpm": 96},   # Vuelta a normal
# ]

# Generar un punto de datos aleatorio y coherente
def generate_random_data_point():
    # Rangos coherentes para un animal sano
    temp_min, temp_max = 37.5, 39.2  # Temperatura en Celsius
    fc_min, fc_max = 70, 120      # Frecuencia cardíaca en lpm

    # Simular algunas anomalías ocasionales para demostración
    if random.random() < 0.1:  # 10% de probabilidad de fiebre
        temp = round(random.uniform(39.5, 41.0), 1)
    else:
        temp = round(random.uniform(temp_min, temp_max), 1)

    if random.random() < 0.1:  # 10% de probabilidad de taquicardia
        fc = random.randint(130, 180)
    else:
        fc = random.randint(fc_min, fc_max)

    timestamp = datetime.now().isoformat(timespec='seconds')

    return {
        "timestamp": timestamp,
        "temperatura_celsius": temp,
        "frecuencia_cardiaca_lpm": fc
    }

# Almacenar los últimos 50 puntos de datos para la tendencia
DATA_HISTORY = []
MAX_HISTORY_SIZE = 50

@iot_data_bp.route("/data", methods=["GET"])
@cross_origin()
def get_all_data():
    """Obtener todos los datos simulados del animal (historial)"""
    try:
        # Asegurarse de que haya al menos un punto de datos si el historial está vacío
        if not DATA_HISTORY:
            DATA_HISTORY.append(generate_random_data_point())

        return jsonify({
            "success": True,
            "data": DATA_HISTORY,
            "total_records": len(DATA_HISTORY)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@iot_data_bp.route("/data/latest", methods=["GET"])
@cross_origin()
def get_latest_data():
    """Obtener los últimos datos del animal"""
    try:
        new_data_point = generate_random_data_point()
        DATA_HISTORY.append(new_data_point)
        if len(DATA_HISTORY) > MAX_HISTORY_SIZE:
            DATA_HISTORY.pop(0)  # Eliminar el punto de datos más antiguo

        return jsonify({
            "success": True,
            "data": new_data_point
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@iot_data_bp.route("/data/anomalies", methods=["GET"])
@cross_origin()
def get_anomalies():
    """Detectar y devolver anomalías en los datos"""
    try:
        # Definir rangos normales
        temp_normal_min, temp_normal_max = 37.5, 39.2
        fc_normal_min, fc_normal_max = 70, 120
        
        # Detectar anomalías en el historial
        anomalies = []
        for data_point in DATA_HISTORY:
            temp = data_point["temperatura_celsius"]
            fc = data_point["frecuencia_cardiaca_lpm"]
            
            if temp < temp_normal_min or temp > temp_normal_max:
                anomaly_type = "Hipotermia" if temp < temp_normal_min else "Fiebre"
                anomalies.append({
                    "timestamp": data_point["timestamp"],
                    "type": "Temperatura",
                    "subtype": anomaly_type,
                    "value": temp,
                    "normal_range": f"{temp_normal_min}-{temp_normal_max}°C"
                })
            
            if fc < fc_normal_min or fc > fc_normal_max:
                anomaly_type = "Bradicardia" if fc < fc_normal_min else "Taquicardia"
                anomalies.append({
                    "timestamp": data_point["timestamp"],
                    "type": "Frecuencia Cardíaca",
                    "subtype": anomaly_type,
                    "value": fc,
                    "normal_range": f"{fc_normal_min}-{fc_normal_max} lpm"
                })
        
        return jsonify({
            "success": True,
            "anomalies": anomalies,
            "total_anomalies": len(anomalies)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@iot_data_bp.route("/status", methods=["GET"])
@cross_origin()
def get_device_status():
    """Simular el estado del dispositivo IoT"""
    return jsonify({
        "success": True,
        "device_status": {
            "online": True,
            "battery_level": 85,
            "signal_strength": "Strong",
            "last_update": datetime.now().isoformat(timespec='seconds') + 'Z',
            "device_id": "IOT_ANIMAL_001"
        }
    })
