from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = 'clave_super_secreta'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Base de datos simulada
usuarios = {
    'admin': {'password': '12345'}, 
    'johndoe': {'password': 'secreto'}
    }

# Clase de Usuario
class Usuario(UserMixin):
    def __init__(self, username, role=None):
        self.id = username
        self.role = role

# Cargar usuario desde la sesión
@login_manager.user_loader
def load_user(username):
    user = usuarios.get(username)
    if user:
        return user(username, user["role"])
    return None

# Ruta principal protegida
@app.route('/')
@login_required
def home():
    return render_template('home.html.jinja2', nombre=current_user.id)

# Ruta de login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = usuarios.get(username)
        if user and check_password_hash(user["password"], password):
            login_user(Usuario(username, user["role"]))
            flash("Inicio de sesión exitoso.", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Usuario o contraseña incorrectos.", "danger")
    return render_template("login.html.jinja2")

# Ruta de logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada exitosamente.", "info")
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(debug=True) 