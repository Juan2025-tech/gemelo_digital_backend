from flask import Flask, jsonify
from flask_cors import CORS
import random
from datetime import datetime

app = Flask(__name__)

CORS(app,
     resources={r"/*": {"origins": "https://gemelodigitalanimal.netlify.app"}},
     supports_credentials=True,
     methods=["GET", "POST", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"])

DATA_HISTORY = []
MAX_HISTORY_SIZE = 50

def generate_random_data_point():
    temp_min, temp_max = 37.5, 39.2
    fc_min, fc_max = 70, 120
    if random.random() < 0.1:
        temp = round(random.uniform(39.5, 41.0), 1)
    else:
        temp = round(random.uniform(temp_min, temp_max), 1)
    if random.random() < 0.1:
        fc = random.randint(130, 180)
    else:
        fc = random.randint(fc_min, fc_max)
    timestamp = datetime.now().isoformat(timespec='seconds')
    return {
        "timestamp": timestamp,
        "temperatura_celsius": temp,
        "frecuencia_cardiaca_lpm": fc
    }

@app.route("/api/iot/data", methods=["GET"])
def get_all_data():
    if not DATA_HISTORY:
        DATA_HISTORY.append(generate_random_data_point())
    return jsonify({"success": True, "data": DATA_HISTORY, "total_records": len(DATA_HISTORY)})

@app.route("/api/iot/data/latest", methods=["GET"])
def get_latest_data():
    new_data_point = generate_random_data_point()
    DATA_HISTORY.append(new_data_point)
    if len(DATA_HISTORY) > MAX_HISTORY_SIZE:
        DATA_HISTORY.pop(0)
    return jsonify({"success": True, "data": new_data_point})

@app.route("/api/iot/anomalies", methods=["GET"])
def get_anomalies():
    temp_normal_min, temp_normal_max = 37.5, 39.2
    fc_normal_min, fc_normal_max = 70, 120
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
    return jsonify({"success": True, "anomalies": anomalies, "total_anomalies": len(anomalies)})

@app.route("/api/iot/status", methods=["GET"])
def get_device_status():
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)


