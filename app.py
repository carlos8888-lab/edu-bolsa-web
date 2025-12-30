import os
from flask import Flask, render_template, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User
from forms import RegisterForm, LoginForm

from pathlib import Path
from datetime import timedelta


def get_secret_key() -> str:
    # 1) Variable de entorno
    key = os.environ.get("SECRET_KEY")
    if key and key.strip():
        return key.strip()

    # 2) Archivo local
    secret_file = Path(r"D:\programacion\no copiar\bolsaweb.txt")
    if secret_file.exists():
        file_key = secret_file.read_text(encoding="utf-8").strip()
        if file_key:
            return file_key

    raise RuntimeError("No se ha encontrado SECRET_KEY ni en el sistema ni en el archivo bolsaweb.txt")


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = get_secret_key()

    # Sesiones: duración
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)
    app.config["SESSION_REFRESH_EACH_REQUEST"] = True

    # DB
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(BASE_DIR, "database.db")

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    print("DB URI:", app.config["SQLALCHEMY_DATABASE_URI"])
    print("CWD:", os.getcwd())

    # Cookies
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_SECURE"] = bool(os.environ.get("HTTPS", ""))  # True solo si hay HTTPS real

    app.config["REMEMBER_COOKIE_HTTPONLY"] = True
    app.config["REMEMBER_COOKIE_SAMESITE"] = "Lax"
    app.config["REMEMBER_COOKIE_SECURE"] = bool(os.environ.get("HTTPS", ""))

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "index"

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    with app.app_context():
        db.create_all()

    @app.get("/")
    def index():
        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))
        return render_template("index.html", login_form=LoginForm(), register_form=RegisterForm())

    @app.post("/register")
    def register():
        form = RegisterForm()
        if not form.validate_on_submit():
            flash("Revisa usuario y contraseña (mínimo 10).", "error")
            return redirect(url_for("index"))

        username = form.username.data.strip()

        # Comprobar que el usuario no exista
        if User.query.filter_by(username=username).first():
            flash("Ese usuario ya está registrado.", "error")
            return redirect(url_for("index"))

        user = User(
            username=username,
            password_hash=generate_password_hash(form.password.data),
        )
        db.session.add(user)
        db.session.commit()

        flash("Cuenta creada. Ya puedes iniciar sesión.", "success")
        return redirect(url_for("index"))

    @app.post("/login")
    def login():
        form = LoginForm()
        if not form.validate_on_submit():
            flash("Datos inválidos.", "error")
            return redirect(url_for("index"))

        username = form.username.data.strip()
        user = User.query.filter_by(username=username).first()

        # Comprobar usuario + contraseña
        if not user or not check_password_hash(user.password_hash, form.password.data):
            flash("Usuario o contraseña incorrectos.", "error")
            return redirect(url_for("index"))

        session.permanent = True
        login_user(user)
        return redirect(url_for("dashboard"))

    @app.get("/dashboard")
    @login_required
    def dashboard():
        return render_template("dashboard.html")

    @app.get("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("index"))

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5556, debug=False)
