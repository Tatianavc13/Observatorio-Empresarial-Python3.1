from datetime import datetime
from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default="editor")  # admin|editor
    active = db.Column(db.Boolean, default=True)

    def set_password(self, password: str):
        # Almacenar contraseña en texto plano (no recomendado en producción)
        self.password_hash = password

    def check_password(self, password: str) -> bool:
        # Comparar directamente en texto plano
        return (self.password_hash or "") == (password or "")

class Flash(db.Model):
    __tablename__ = "flashes"
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    entity = db.Column(db.String(255))
    link = db.Column(db.String(512))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    location = db.Column(db.String(255))
    cost = db.Column(db.String(100))
    modality = db.Column(db.String(60))  # Virtual|Presencial|Híbrido
    schedule = db.Column(db.String(120))
    deadline = db.Column(db.Date)
    visible = db.Column(db.Boolean, default=True)
    featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Company(db.Model):
    __tablename__ = "companies"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    headquarter = db.Column(db.String(255))
    phone = db.Column(db.String(50))
    website_url = db.Column(db.String(512))
    logo_url = db.Column(db.String(512))
