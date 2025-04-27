from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

app = Flask(__name__)
app.secret_key = "secretkey"  # Necesario para usar WTForms


class RegistrationForm(FlaskForm):
    nombre = StringField("Nombre", validators=[
        DataRequired(message="El nombre es obligatorio."),
        Length(min=3, message="El nombre debe tener al menos 3 caracteres.")
    ])
    correo = StringField("Correo", validators=[
        DataRequired(message="El correo es obligatorio."),
        Email(message="Debe ser un correo válido.")
    ])
    contraseña = PasswordField("Contraseña", validators=[
        DataRequired(message="La contraseña es obligatoria."),
        Length(min=6, message="La contraseña debe tener al menos 6 caracteres.")
    ])
    submit = SubmitField("Registrar")

@app.route("/")
def home():
    return redirect(url_for("register"))

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        correo = form.correo.data
        flash(f"Usuario {nombre} registrado con éxito.", "success")
        return redirect(url_for("register"))
    return render_template("register.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)