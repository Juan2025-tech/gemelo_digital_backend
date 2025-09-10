from flask import Flask, jsonify
from flask_cors import CORS
from .routes.iot_data import iot_data_bp

app = Flask(__name__)
CORS(app) # Habilitar CORS para todas las rutas

app.register_blueprint(iot_data_bp, url_prefix=\"/api/iot\")

@app.route(\"/test\")
def test_route():
    return jsonify({"message": "Test route works!"})

if __name__ == \"__main__\":
    app.run(host=\"0.0.0.0\", port=5000, debug=True)


