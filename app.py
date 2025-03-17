from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key'  
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI','postgresql://biblioteca_owner:npg_oh3myqZSAT8g@ep-shy-tree-a5nwg95y-pooler.us-east-2.aws.neon.tech/biblioteca?sslmode=require')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Configuración de Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# MODELOS

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    # Un usuario puede tener muchos libros prestados
    libros = db.relationship('Libro', backref='usuario', lazy=True)

class Libro(db.Model):
    __tablename__ = 'libro'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    autor = db.Column(db.String(150), nullable=False)
    fecha_publicacion = db.Column(db.Date, nullable=False)
    # 'disponible' o 'no disponible'
    estado = db.Column(db.String(50), nullable=False, default='disponible')
    # Relación con el usuario (si está prestado)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=True)
    # Fecha límite para la devolución (asignada al prestar)
    fecha_devolucion = db.Column(db.Date, nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# RUTAS

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('buscar'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('buscar'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = Usuario.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('buscar'))
        else:
            flash('Credenciales incorrectas', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('buscar'))
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        password = request.form.get('password')
        if Usuario.query.filter_by(email=email).first():
            flash('El email ya está registrado.', 'warning')
            return redirect(url_for('register'))
        hashed_password = generate_password_hash(password)
        new_user = Usuario(nombre=nombre, apellido=apellido, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registro exitoso, inicia sesión.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('login'))


@app.route('/buscar', methods=['GET', 'POST'])
@login_required
def buscar():
    search_results = None
    if request.method == 'POST':
        criterio = request.form.get('criterio')
        search_results = Libro.query.filter(
            (Libro.nombre.ilike(f'%{criterio}%')) | (Libro.autor.ilike(f'%{criterio}%'))
        ).all()
    page = request.args.get('page', 1, type=int)
    libros_paginated = Libro.query.order_by(Libro.id).paginate(page=page, per_page=10, error_out=False)
    borrowed_books = Libro.query.filter_by(usuario_id=current_user.id).all()
    return render_template(
        'buscar.html',
        search_results=search_results,
        libros_paginated=libros_paginated,
        borrowed_books=borrowed_books
    )


@app.route('/prestar/<int:libro_id>')
@login_required
def prestar(libro_id):
    libro = Libro.query.get_or_404(libro_id)
    if libro.estado == 'disponible':
        libro.estado = 'no disponible'
        libro.usuario_id = current_user.id
        libro.fecha_devolucion = datetime.utcnow().date() + timedelta(days=7)
        db.session.commit()
        flash(f'Has prestado el libro "{libro.nombre}". Devuélvelo antes del {libro.fecha_devolucion}', 'success')
    else:
        flash('El libro no está disponible para préstamo.', 'danger')
    return redirect(url_for('buscar'))

@app.route('/devolver/<int:libro_id>')
@login_required
def devolver(libro_id):
    libro = Libro.query.get_or_404(libro_id)
    if libro.usuario_id == current_user.id:
        libro.estado = 'disponible'
        libro.usuario_id = None
        libro.fecha_devolucion = None
        db.session.commit()
        flash(f'Has devuelto el libro "{libro.nombre}". Gracias.', 'success')
    else:
        flash('No tienes este libro prestado.', 'warning')
    return redirect(url_for('buscar'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV', 'development') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
