from flask import Flask
from flask_cors import CORS
from .routes.iot_data import iot_data_bp

app = Flask(__name__, static_folder='static', static_url_path='/')
CORS(app) # Habilitar CORS para todas las rutas

app.register_blueprint(iot_data_bp, url_prefix='/api/iot')

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


