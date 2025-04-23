from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/info", methods=["GET"])
def home(): 
    return "Bienvenidos a mi API"

@app.route("/mensaje", methods=["POST"])
def saludo():
    
    data = request.json
    nombre = data.get("nombre", "Usuario")

    return f"Hola, min nombre es {nombre} y este es una ruta de mi server de flask!"

if __name__ == "__main__":
    app.run(debug=True)