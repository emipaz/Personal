from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from datetime import datetime

class Certificado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    fecha = db.Column(db.Date, nullable=True)
    descripcion = db.Column(db.Text, nullable=True)
    institucion = db.Column(db.String(150), nullable=True)
    imagen_url = db.Column(db.String(300), nullable=False)  # preview
    pdf_url = db.Column(db.String(300), nullable=False)