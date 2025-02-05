from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import re

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True, index=True)
    phone = db.Column(db.String(10), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')  # 'farmer', 'broker', 'admin'
    password_hash = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    # Relationship with Livestock
    livestock = db.relationship("Livestock", back_populates="owner", cascade="all, delete-orphan")

    @property
    def is_farmer(self):
        return self.role == 'farmer'
        
    @property
    def is_broker(self):
        return self.role == 'broker'

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        if not self.is_valid_password(password):
            raise ValueError("Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one number")
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def is_valid_password(password):
        if len(password) < 8:
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'\d', password):
            return False
        return True

    @staticmethod
    def is_valid_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def is_valid_phone(phone):
        return bool(re.match(r'^\d{10}$', phone))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class Livestock(db.Model):
    __tablename__ = 'livestock'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    breed = db.Column(db.String(100), nullable=False)
    age = db.Column(db.String(50), nullable=False)
    weight = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(250), nullable=False)
    image = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    
    # Foreign key to User
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    # Relationship with User
    owner = db.relationship("User", back_populates="livestock")

    def to_dict(self):
        return {
            'id': self.id,
            'breed': self.breed,
            'age': self.age,
            'weight': self.weight,
            'price': self.price,
            'location': self.location,
            'image': self.image,
            'description': self.description,
            'owner_id': self.owner_id,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        return f"<Livestock id={self.id}, breed={self.breed}, owner_id={self.owner_id}>"
