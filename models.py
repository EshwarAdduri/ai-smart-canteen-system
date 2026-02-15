from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')  # 'student' or 'admin'
    department = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    reservations = db.relationship('Reservation', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return f'<User {self.username}>'


class Meal(db.Model):
    __tablename__ = 'meals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # breakfast, lunch, dinner, snack
    stock = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(255))
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    reservations = db.relationship('Reservation', backref='meal', lazy='dynamic')
    predictions = db.relationship('Prediction', backref='meal', lazy='dynamic')

    def update_stock(self, quantity):
        self.stock += quantity
        if self.stock <= 0:
            self.stock = 0
            self.is_available = False
        else:
            self.is_available = True
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category': self.category,
            'stock': self.stock,
            'is_available': self.is_available,
            'image_url': self.image_url or '/static/images/default-meal.jpg'
        }

    def __repr__(self):
        return f'<Meal {self.name}>'


class Reservation(db.Model):
    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), nullable=False, index=True)
    pickup_time = db.Column(db.DateTime, nullable=False, index=True)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, completed, cancelled
    token = db.Column(db.String(10), unique=True, nullable=False)
    quantity = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def generate_token(self):
        self.token = secrets.token_hex(4).upper()

    def cancel(self):
        if self.status == 'pending':
            self.status = 'cancelled'
            # Return stock
            meal = Meal.query.get(self.meal_id)
            if meal:
                meal.update_stock(self.quantity)
            db.session.commit()
            return True
        return False

    def complete(self):
        self.status = 'completed'
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'meal_name': self.meal.name,
            'pickup_time': self.pickup_time.strftime('%Y-%m-%d %H:%M'),
            'status': self.status,
            'token': self.token,
            'quantity': self.quantity
        }

    def __repr__(self):
        return f'<Reservation {self.token}>'


class Prediction(db.Model):
    __tablename__ = 'predictions'

    id = db.Column(db.Integer, primary_key=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, index=True)
    time_slot = db.Column(db.String(20), nullable=False)  # breakfast, lunch, dinner
    predicted_demand = db.Column(db.Integer, nullable=False)
    actual_demand = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Prediction Meal:{self.meal_id} Date:{self.date}>'


class RushHour(db.Model):
    __tablename__ = 'rush_hours'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, index=True)
    hour = db.Column(db.Integer, nullable=False)  # 0-23
    traffic_count = db.Column(db.Integer, default=0)
    rush_level = db.Column(db.String(20))  # low, medium, high
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<RushHour {self.date} {self.hour}:00>'
