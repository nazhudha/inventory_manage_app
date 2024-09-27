from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app.extensions import db 

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # 'admin' or 'regular'
    
    # Relationship to equipment
    equipment = db.relationship('Equipment', backref='owner', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    # Foreign key linking to the User table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'<Asset {self.name}>'