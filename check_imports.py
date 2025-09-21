import sys

print("=== Información de entorno ===")
print("Python ejecutado desde:", sys.executable)
print("Versión:", sys.version)
print("Rutas de búsqueda de módulos (sys.path):")
for p in sys.path:
    print(" -", p)

print("\n=== Prueba de importación ===")
try:
    import flask
    print("✅ Flask encontrado en:", flask.__file__)
except ImportError as e:
    print("❌ Flask no encontrado:", e)

try:
    import flask_cors
    print("✅ Flask-Cors encontrado en:", flask_cors.__file__)
except ImportError as e:
    print("❌ Flask-Cors no encontrado:", e)
