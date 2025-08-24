import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'tu_clave_secreta')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE', 'credenciales.json')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')
