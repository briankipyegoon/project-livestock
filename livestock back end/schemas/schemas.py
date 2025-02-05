from config.config2 import ma
from models.models import User, Livestock
from marshmallow import validates, ValidationError, fields, validate

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True
        exclude = ('password_hash', 'is_deleted', 'deleted_at')  # Hide sensitive/internal fields
    
    # Add password field for input only
    password = fields.String(load_only=True, required=True)
    
    # Add nested relationships
    livestock = ma.Nested('LivestockSchema', many=True, exclude=('owner',))

    @validates('email')
    def validate_email(self, email):
        if not User.is_valid_email(email):
            raise ValidationError('Invalid email format')

    @validates('phone')
    def validate_phone(self, phone):
        if not User.is_valid_phone(phone):
            raise ValidationError('Phone number must be 10 digits')

    @validates('password')
    def validate_password(self, password):
        if not User.is_valid_password(password):
            raise ValidationError(
                'Password must be at least 8 characters and contain at least '
                'one uppercase letter, one lowercase letter, and one number'
            )

class LivestockSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Livestock
        include_relationships = True
        load_instance = True
        exclude = ('is_deleted', 'deleted_at')

    id = fields.Int(dump_only=True)
    breed = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    age = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    weight = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    price = fields.Float(required=True, validate=validate.Range(min=0))
    location = fields.Str(required=True, validate=validate.Length(min=1, max=250))
    description = fields.Str(required=True)
    image = fields.Str(dump_only=True)
    owner_id = fields.Int(required=True)

    # Add nested owner details
    owner = ma.Nested('UserSchema', only=('id', 'name', 'phone'), dump_only=True)

    @validates('breed')
    def validate_breed(self, breed):
        if not breed or len(breed.strip()) < 2:
            raise ValidationError('Breed must be at least 2 characters long')

    @validates('price')
    def validate_price(self, price):
        if price <= 0:
            raise ValidationError('Price must be greater than 0')

# Schema instances
user_schema = UserSchema()
users_schema = UserSchema(many=True)
livestock_schema = LivestockSchema()
livestocks_schema = LivestockSchema(many=True) 