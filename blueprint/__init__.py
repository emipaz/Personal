from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session
from models import Certificado, db
import os
from datetime import date
from werkzeug.utils import secure_filename


bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return render_template('index.html')

@bp.route('/miapp')
def miapp():
    return render_template('miapp.html')

@bp.route('/galeria')
def galeria():
    page = request.args.get('page', 1, type=int)
    certificados = Certificado.query.order_by(Certificado.fecha.desc()).paginate(page=page, per_page=6)
    return render_template('galeria.html', certificados=certificados)

@bp.route('/admin/cargar', methods=['GET', 'POST'])
def cargar_certificado():
    # Protección por contraseña simple
    PASSWORD = 'emipaz1975-eNdeglep'
    if 'cert_admin' not in session:
        if request.method == 'POST' and 'password' in request.form:
            if request.form['password'] == PASSWORD:
                session['cert_admin'] = True
                return redirect(url_for('main.cargar_certificado'))
            else:
                flash('Contraseña incorrecta', 'danger')
        return render_template('admin_login.html')
    if request.method == 'POST' and 'nombre' in request.form:
        nombre = request.form['nombre']
        fecha = request.form.get('fecha')
        descripcion = request.form.get('descripcion')
        institucion = request.form.get('institucion')
        imagen = request.files['imagen']
        pdf = request.files['pdf']
        if imagen and pdf:
            imagen_filename = secure_filename(imagen.filename)
            pdf_filename = secure_filename(pdf.filename)
            upload_folder = current_app.config['UPLOAD_FOLDER']
            imagen.save(os.path.join(upload_folder, imagen_filename))
            pdf.save(os.path.join(upload_folder, pdf_filename))
            nuevo = Certificado(
                nombre=nombre,
                fecha=date.fromisoformat(fecha) if fecha else None,
                descripcion=descripcion,
                institucion=institucion,
                imagen_url=f'/static/uploads/{imagen_filename}',
                pdf_url=f'/static/uploads/{pdf_filename}'
            )
            db.session.add(nuevo)
            db.session.commit()
            flash('Certificado cargado correctamente!', 'success')
            return redirect(url_for('main.cargar_certificado'))
    return render_template('admin_cargar.html')