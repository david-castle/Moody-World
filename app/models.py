from app import app, db, login
from datetime import datetime
from flask_login import UserMixin
from time import time
from werkzeug.security import generate_password_hash, check_password_hash

import jwt


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')
    
    @staticmethod
    def veryify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], 
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

class Query(db.Model):
    id = db.Column(db.Integer primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    query_terms = db.Column(db.String(240))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Query {}>'.format(self.body)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))