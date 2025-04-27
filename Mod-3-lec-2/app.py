from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_principal import Principal, Permission, RoleNeed, Identity, identity_changed, identity_loaded, AnonymousIdentity

app = Flask(__name__)
app.secret_key = 'clave_super_secreta'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


principal = Principal(app)
admin_permission = Permission(RoleNeed('admin'))
user_permission = Permission(RoleNeed('user'))


usuarios = {
    'admin': {'password': '12345', 'role': 'admin'},
    'johndoe': {'password': 'secreto', 'role': 'user'}
}


class Usuario(UserMixin):
    def __init__(self, username, role):
        self.id = username
        self.role = role

@login_manager.user_loader
def load_user(username):
    user = usuarios.get(username)
    if user:
        return Usuario(username, user["role"])
    return None

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    identity.user = current_user
    if hasattr(current_user, 'role'):
        identity.provides.add(RoleNeed(current_user.role))


@app.route('/')
@login_required
def home():
    return render_template('home.html.jinja2', nombre=current_user.id)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = usuarios.get(username)
        if user and user["password"] == password:  
            login_user(Usuario(username, user["role"]))
            identity_changed.send(app, identity=Identity(username))
            flash("Inicio de sesión exitoso.", "success")
            return redirect(url_for("home"))
        else:
            flash("Usuario o contraseña incorrectos.", "danger")
    return render_template("login.html.jinja2")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    identity_changed.send(app, identity=AnonymousIdentity())
    flash("Sesión cerrada exitosamente.", "info")
    return redirect(url_for("login"))


@app.route("/admin")
@login_required
@admin_permission.require(http_exception=403)
def admin():
    return render_template("admin.html.jinja2", nombre=current_user.id)


@app.route("/user")
@login_required
@user_permission.require(http_exception=403)
def user_dashboard():
    return render_template("user.html.jinja2", nombre=current_user.id)

if __name__ == '__main__':
    app.run(debug=True)