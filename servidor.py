from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
import bcrypt

# Configuración de la Aplicación 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gestion_tareas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'gestion-app-shh.key'

# Configuración de Cookies de Sesión 
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,  # Previene acceso a la cookie desde JavaScript
    SESSION_COOKIE_SAMESITE='Lax', # Protección contra ataques CSRF
)

db = SQLAlchemy(app)






# Modelos de la Base de Datos
class Usuario(db.Model):
    """Modelo para la tabla de usuarios."""
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(80), unique=True, nullable=False)
    contrasenia_hash = db.Column(db.String(128), nullable=False)

class Tarea(db.Model):
    """Modelo para la tabla de tareas."""
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.String(300), nullable=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    usuario = db.relationship('Usuario', backref=db.backref('tareas', lazy=True))





#Rutas de la API

@app.route('/registro', methods=['POST'])
def registrar_usuario():
    """Endpoint para registrar un nuevo usuario."""
    datos = request.get_json()
    nombre_usuario = datos.get('usuario')
    contrasenia_plana = datos.get('contrasenia')

    if not nombre_usuario or not contrasenia_plana:
        return jsonify({'error': 'El nombre de usuario y la contraseña son requeridos'}), 400

    if Usuario.query.filter_by(nombre_usuario=nombre_usuario).first():
        return jsonify({'error': 'El nombre de usuario ya está en uso'}), 400

    # Hasheo la contraseña 
    contrasenia_bytes = contrasenia_plana.encode('utf-8') # convierto a bytes
    contrasenia_hasheada = bcrypt.hashpw(contrasenia_bytes, bcrypt.gensalt())  # genero la sal y el hash

    nuevo_usuario = Usuario(nombre_usuario=nombre_usuario, contrasenia_hash=contrasenia_hasheada)
    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({'mensaje': 'Usuario registrado exitosamente'}), 201






@app.route('/login', methods=['POST'])
def iniciar_sesion():
    """Endpoint para iniciar sesión y crear una sesión de usuario."""
    datos = request.get_json()
    nombre_usuario = datos.get('usuario')
    contrasenia_plana = datos.get('contrasenia')

    usuario_existente = Usuario.query.filter_by(nombre_usuario=nombre_usuario).first()

    if not usuario_existente:
        return jsonify({'error': 'Credenciales inválidas'}), 401

    # Verificar la contraseña con bcrypt
    contrasenia_plana_bytes = contrasenia_plana.encode('utf-8')
    contrasenia_hash_bytes = usuario_existente.contrasenia_hash

    if not bcrypt.checkpw(contrasenia_plana_bytes, contrasenia_hash_bytes):
        return jsonify({'error': 'Credenciales inválidas'}), 401
    
    # Establecer la sesión del usuario
    session['usuario_id'] = usuario_existente.id
    
    return jsonify({
        'mensaje': f'Inicio de sesión exitoso. ¡Bienvenido, {usuario_existente.nombre_usuario}!',
        'usuario_id': usuario_existente.id
    }), 200





@app.route('/logout', methods=['POST'])
def cerrar_sesion():
    """Endpoint para cerrar la sesión del usuario."""
    session.pop('usuario_id', None)
    return jsonify({'mensaje': 'Sesión cerrada exitosamente'}), 200






@app.route('/tareas', methods=['GET', 'POST'])
def gestionar_tareas():
    """Endpoint para gestionar tareas. GET para obtener, POST para crear."""
    # Verificar si hay un usuario en la sesión
    if 'usuario_id' not in session:
        return jsonify({'error': 'Acceso no autorizado. Por favor, inicie sesión.'}), 401

    usuario_id = session['usuario_id']

    # --- Lógica para CREAR una nueva tarea ---
    if request.method == 'POST':
        datos = request.get_json()
        titulo = datos.get('titulo')

        if not titulo:
            return jsonify({'error': 'El título de la tarea es requerido'}), 400
        
        nueva_tarea = Tarea(
            titulo=titulo,
            descripcion=datos.get('descripcion', ''),
            usuario_id=usuario_id
        )
        db.session.add(nueva_tarea)
        db.session.commit()
        
        return jsonify({
            'mensaje': 'Tarea creada exitosamente',
            'tarea': {'id': nueva_tarea.id, 'titulo': nueva_tarea.titulo, 'descripcion': nueva_tarea.descripcion}
        }), 201

    if request.method == 'GET':
        usuario = db.session.get(Usuario, usuario_id)
        tareas_usuario = Tarea.query.filter_by(usuario_id=usuario_id).all()
        
        # Cntenido dinámico
        contenido_body = f"<h1>¡Bienvenido, {usuario.nombre_usuario}!</h1>"
        if not tareas_usuario:
            contenido_body += "<p>No tienes tareas pendientes. ¡Felicidades!</p>"
        else:
            contenido_body += "<h2>Tus tareas:</h2><ul>"
            for tarea in tareas_usuario:
                contenido_body += f"<li><b>{tarea.titulo}</b>: {tarea.descripcion or 'Sin descripción'}</li>"
            contenido_body += "</ul>"

        # Estructura HTML completa
        html_response = f'''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tareas de {usuario.nombre_usuario}</title>
    <style>
        body {{ font-family: sans-serif; margin: 2em; }}
        ul {{ list-style-type: square; }}
    </style>
</head>
<body>
    {contenido_body}
</body>
</html>
'''
        from flask import make_response
        respuesta = make_response(html_response)
        respuesta.headers['Content-Type'] = 'text/html'
        return respuesta






# --- Inicialización  del Servidor---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea las tablas si no existen
        print("Base de datos y tablas creadas.")
    app.run(debug=True)