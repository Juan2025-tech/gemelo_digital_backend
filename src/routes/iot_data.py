from flask import Blueprint, jsonify
import pandas as pd
import json
import os
from flask_cors import cross_origin

iot_data_bp = Blueprint('iot_data', __name__)

@iot_data_bp.route('/data', methods=['GET'])
@cross_origin()
def get_all_data():
    """Obtener todos los datos simulados del animal"""
    try:
        # Leer el archivo CSV con los datos simulados
        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'datos_simulados_animal.csv')
        df = pd.read_csv(csv_path)
        
        # Convertir a formato JSON
        data = df.to_dict('records')
        
        return jsonify({
            'success': True,
            'data': data,
            'total_records': len(data)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@iot_data_bp.route('/data/latest', methods=['GET'])
@cross_origin()
def get_latest_data():
    """Obtener los últimos datos del animal"""
    try:
        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'datos_simulados_animal.csv')
        df = pd.read_csv(csv_path)
        
        # Obtener el último registro
        latest_data = df.iloc[-1].to_dict()
        
        return jsonify({
            'success': True,
            'data': latest_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@iot_data_bp.route('/data/anomalies', methods=['GET'])
@cross_origin()
def get_anomalies():
    """Detectar y devolver anomalías en los datos"""
    try:
        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'datos_simulados_animal.csv')
        df = pd.read_csv(csv_path)
        
        # Definir rangos normales
        temp_normal_min, temp_normal_max = 37.5, 39.2
        fc_normal_min, fc_normal_max = 70, 120
        
        # Detectar anomalías
        anomalies = []
        for index, row in df.iterrows():
            temp = row['temperatura_celsius']
            fc = row['frecuencia_cardiaca_lpm']
            
            if temp < temp_normal_min or temp > temp_normal_max:
                anomaly_type = 'Hipotermia' if temp < temp_normal_min else 'Fiebre'
                anomalies.append({
                    'timestamp': row['timestamp'],
                    'type': 'Temperatura',
                    'subtype': anomaly_type,
                    'value': temp,
                    'normal_range': f'{temp_normal_min}-{temp_normal_max}°C'
                })
            
            if fc < fc_normal_min or fc > fc_normal_max:
                anomaly_type = 'Bradicardia' if fc < fc_normal_min else 'Taquicardia'
                anomalies.append({
                    'timestamp': row['timestamp'],
                    'type': 'Frecuencia Cardíaca',
                    'subtype': anomaly_type,
                    'value': fc,
                    'normal_range': f'{fc_normal_min}-{fc_normal_max} lpm'
                })
        
        return jsonify({
            'success': True,
            'anomalies': anomalies,
            'total_anomalies': len(anomalies)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@iot_data_bp.route('/status', methods=['GET'])
@cross_origin()
def get_device_status():
    """Simular el estado del dispositivo IoT"""
    return jsonify({
        'success': True,
        'device_status': {
            'online': True,
            'battery_level': 85,
            'signal_strength': 'Strong',
            'last_update': '2025-08-30T12:00:00Z',
            'device_id': 'IOT_ANIMAL_001'
        }
    })

