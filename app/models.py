import base64
import os
from app import db, login
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    cart = db.relationship("Cart", backref="user", lazy="dynamic")
    fridge = db.relationship("Fridge", backref="user", lazy="dynamic")
    recipes = db.relationship("Recipes", backref="user", lazy="dynamic")

    token = db.Column(db.String(32), index=True, unique= True)
    token_expiration = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_password(kwargs['password'])
        db.session.add(self)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password, password)


    def set_password(self,password):
        self.password = generate_password_hash(password)
        db.session.commit()

    def to_dict(self):
        return{
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "date_created": self.date_created,
            "password": self.password
        }
    
    def get_token(self, expires_in=10000):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.commit()
        return self.token
    
    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)
        db.session.commit()

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.String(50), nullable=False)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()
    
    def to_dict(self):
        return{
            "id": self.id,
            "item": self.item,
            "quantity": self.quantity
        }

class Fridge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.String(50), nullable=False)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()
    
    def to_dict(self):
        return{
            "id": self.id,
            "item": self.item,
            "quantity": self.quantity
        }

class Recipes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe = db.Column(db.String(10000), nullable = False)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()
    
    def to_dict(self):
        return{
            "id": self.id,
            "recipe": self.recipe,
        }