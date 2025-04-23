from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    print("Index route accessed")
    data = {"title": "Bienvenidos", "message": "¡Hola, Flask con Jinja2!"}
    return render_template('index.html', data=data)

@app.route("/page1")
def page1():
    items = ["Elemento 1", "Elemento 2", "Elemento 3"]
    return render_template("page1.html", title="Página 1", items=items)

@app.route("/page2")
def page2():
    users = [
        {"nombre": "Xavier", "correo": "xavier@example.com"},
        {"nombre": "Maria", "correo": "maria@example.com"},
        {"nombre": "Luis", "correo": "luis@example.com"}
    ]
    return render_template("page2.html", title="Página 2", users=users)

if __name__ == '__main__':
    app.run(debug=True)