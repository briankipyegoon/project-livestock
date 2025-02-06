from config.config import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import re
from sqlalchemy.ext.hybrid import hybrid_property

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True, index=True)
    phone = db.Column(db.String(10), nullable=False)
    role = db.Column(db.String(100), nullable=False)  
    password_hash = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    farmer = db.relationship("Farmer", back_populates="user", uselist=False, 
                           cascade="all, delete-orphan")
    broker = db.relationship("broker", back_populates="user", uselist=False,
                             cascade="all, delete-orphan")

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
        """Password must be at least 8 characters and contain at least one uppercase, one lowercase, and one number"""
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
        """Basic email validation"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def is_valid_phone(phone):
        """Phone must be 10 digits"""
        return bool(re.match(r'^\d{10}$', phone))

    def soft_delete(self):
        """Soft delete the user"""
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()
        self.is_active = False

    def restore(self):
        """Restore a soft-deleted user"""
        self.is_deleted = False
        self.deleted_at = None
        self.is_active = True

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        return f"<User id={self.id}, name={self.name}, email={self.email}, role={self.role}>"

class Farmer(db.Model):
    __tablename__ = 'farmer'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, unique=True)
    farm_name = db.Column(db.String(250), nullable=False, index=True)
    farm_location = db.Column(db.String(250))
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
 
    user = db.relationship("User", back_populates="farmer")
    livestock = db.relationship("livestock", back_populates="farmer", cascade="all, delete-orphan")

    def soft_delete(self):
        """Soft delete the farmer"""
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()
        self.is_active = False

    def restore(self):
        """Restore a soft-deleted farmer"""
        self.is_deleted = False
        self.deleted_at = None
        self.is_active = True

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'farm_location': self.farm_location,
            'is_active': self.is_active,
            'created_at': self.created_at
        }

    def __repr__(self):
        return f"<Farmer id={self.id}, user_id={self.user_id}>"

class broker(db.Model):
    __tablename__ = 'broker'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, unique=True)
    company_name = db.Column(db.String(250), nullable=False, index=True)
    address = db.Column(db.String(250))
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    
    user = db.relationship("User", back_populates="broker")

    def soft_delete(self):
        """Soft delete the broker"""
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()
        self.is_active = False

    def restore(self):
        """Restore a soft-deleted broker"""
        self.is_deleted = False
        self.deleted_at = None
        self.is_active = True

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'company_name': self.company_name,
            'address': self.address,
            'is_active': self.is_active,
            'created_at': self.created_at
        }

    def __repr__(self):
        return f"<broker id={self.id}, user_id={self.user_id}, company_name={self.company_name}>"

class livestock(db.Model):
    __tablename__ = 'livestock'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    livestock = db.Column(db.String(250), nullable=False, index=True)
    breed = db.Column(db.Float, nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    image_url = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(250), nullable=False)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmer.id', ondelete='CASCADE'), nullable=True)
    
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    farmer = db.relationship("Farmer", back_populates="livestock")

    def soft_delete(self):
        """Soft delete the livestock"""
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()
        self.is_active = False

    def restore(self):
        """Restore a soft-deleted livestock"""
        self.is_deleted = False
        self.deleted_at = None
        self.is_active = True

    def to_dict(self):
        return {
            'id': self.id,
            'livestock': self.livestock,
            'breed': self.breed,
            'phone': self.phone,
            'image_url': self.image_url,
            'description': self.description,
            'location': self.location,
            'farmer_id': self.farmer_id,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        return f"<livestock id={self.id}, livestock={self.livestock}, farmer_id={self.farmer_id}>"