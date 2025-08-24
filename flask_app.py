
from flask import Flask, render_template, redirect, url_for, request, send_from_directory, flash
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import date
from werkzeug.utils import secure_filename
from models import db
from flask_migrate import Migrate
from blueprint import bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///certificados.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'tu_clave_secreta'
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
db.init_app(app)


app.register_blueprint(bp)

# @app.route('/')
# def home():
#     return render_template('index.html')

# # Ruta para galería de certificados
# @app.route('/galeria')
# def galeria():
#     page = request.args.get('page', 1, type=int)
#     certificados = Certificado.query.order_by(Certificado.fecha.desc()).paginate(page=page, per_page=6)
#     return render_template('galeria.html', certificados=certificados)

# # Ruta admin para cargar certificados (solo para ti)
# @app.route('/admin/cargar', methods=['GET', 'POST'])
# def cargar_certificado():
#     # Aquí podrías agregar autenticación básica si lo deseas
#     if request.method == 'POST':
#         nombre = request.form['nombre']
#         fecha = request.form.get('fecha')
#         descripcion = request.form.get('descripcion')
#         institucion = request.form.get('institucion')
#         imagen = request.files['imagen']
#         pdf = request.files['pdf']
#         if imagen and pdf:
#             imagen_filename = secure_filename(imagen.filename)
#             pdf_filename = secure_filename(pdf.filename)
#             imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], imagen_filename))
#             pdf.save(os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename))
#             nuevo = Certificado(
#                 nombre=nombre,
#                 fecha=date.fromisoformat(fecha) if fecha else None,
#                 descripcion=descripcion,
#                 institucion=institucion,
#                 imagen_url=f'/static/uploads/{imagen_filename}',
#                 pdf_url=f'/static/uploads/{pdf_filename}'
#             )
#             db.session.add(nuevo)
#             db.session.commit()
#             flash('Certificado cargado correctamente!', 'success')
#             return redirect(url_for('cargar_certificado'))
#     return render_template('admin_cargar.html')

# @app.route('/static/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

migrate = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
