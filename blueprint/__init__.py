from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session
from models import Certificado, db
import os
from datetime import date
from werkzeug.utils import secure_filename
import requests
from functools import lru_cache
from datetime import datetime, timedelta
import pytz


@lru_cache(maxsize=32)
def obtener_cotizacion(moneda):
    if moneda in ['oficial', 'blue', 'mep', 'contadoconliqui', 'tarjeta', 'mayorista', 'cripto']:
        r = requests.get('https://dolarapi.com/v1/dolares')
        if r.ok:
            data = r.json()
            cotizacion = next((d for d in data if d['nombre'].lower() == moneda), None)
            return cotizacion
    else:
        r = requests.get(f'https://dolarapi.com/v1/cotizaciones/{moneda}')
        if r.ok:
            data = r.json()
            return data
    return None


def obtener_cotizacion_con_cache(moneda):
    cotizacion = obtener_cotizacion(moneda)
    if cotizacion and 'fechaActualizacion' in cotizacion:
        # Convertir la fecha a Buenos Aires
        fecha_api_utc = datetime.strptime(cotizacion['fechaActualizacion'], '%Y-%m-%dT%H:%M:%S.%fZ')

        
        # ahora_bsas = datetime.now(pytz.timezone('America/Argentina/Buenos_Aires'))
        zona_horaria_buenos_aires = pytz.timezone('America/Argentina/Buenos_Aires')
        fecha_api_bsas = datetime.fromisoformat(cotizacion.get('fechaActualizacion', '')).astimezone(zona_horaria_buenos_aires)
        ahora_buenos_aires = datetime.now(zona_horaria_buenos_aires)
        # Si han pasado más de 1 hora, limpiar el cache y volver a llamar
        if (ahora_buenos_aires - fecha_api_bsas) > timedelta(hours=1):
            obtener_cotizacion.cache_clear()
            cotizacion = obtener_cotizacion(moneda)
    return cotizacion



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



@bp.route('/conversor', methods=['GET', 'POST'])
def conversor():
    monedas = {
        'oficial': 'Dólar Oficial',
        'blue': 'Dólar Blue',
        'mep': 'Dólar MEP',
        'contadoconliqui': 'Dólar Contado con Liquidación',
        'tarjeta': 'Dólar Tarjeta',
        'mayorista': 'Dólar Mayorista',
        'cripto': 'Dólar Cripto',
        'eur': 'Euro',
        'brl': 'Real',
        'clp': 'Peso Chileno',
        'uyu': 'Peso Uruguayo'
    }
    resultado = None
    tasa_compra = None
    tasa_venta = None
    moneda_seleccionada = None
    sentido = None

    if request.method == 'POST':
        moneda = request.form['moneda']
        monto = float(request.form['monto'])
        sentido = request.form['sentido']
        cotizacion = obtener_cotizacion_con_cache(moneda)
        if cotizacion:
            tasa_compra = cotizacion.get('compra', 0)
            tasa_venta = cotizacion.get('venta', 0)
        # Dólares usan endpoint especial
        # if moneda in ['oficial', 'blue', 'mep', 'contadoconliqui', 'tarjeta', 'mayorista', 'cripto']:
        #     r = requests.get('https://dolarapi.com/v1/dolares')
        #     if r.ok:
        #         data = r.json()
        #         cotizacion = next((d for d in data if d['nombre'].lower() == moneda), None)
        #         if cotizacion:
        #             tasa_compra = cotizacion.get('compra', 0)
        #             tasa_venta = cotizacion.get('venta', 0)
        # else:
        #     r = requests.get(f'https://dolarapi.com/v1/cotizaciones/{moneda}')
        #     if r.ok:
        #         data = r.json()
        #         tasa_compra = data.get('compra', 0)
        #         tasa_venta = data.get('venta', 0)
        moneda_seleccionada = monedas.get(moneda, moneda)
        # Conversión según sentido
        if tasa_compra and tasa_venta:
            if sentido == 'ars_a_moneda':
                resultado = monto / tasa_venta
            elif sentido == 'moneda_a_ars':
                resultado = monto * tasa_compra
    return render_template('conversor.html',
                           monedas=monedas,
                           resultado=resultado,
                           tasa_compra=tasa_compra,
                           tasa_venta=tasa_venta,
                           moneda_seleccionada=moneda_seleccionada,
                           sentido=sentido)