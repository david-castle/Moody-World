from app import app, db, login
from datetime import datetime
from flask_login import UserMixin
from time import time
from werkzeug.security import generate_password_hash, check_password_hash

import jwt


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    firstname = db.Column(db.String(120), index=True, unique=True)
    lastname = db.Column(db.String(120), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return str(self.id)
        #return '{}'.format(int(self.id))
    
    def is_authenticated(self):
        return True
        
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
        
    def get_id(self):
        return str(self.id)
    
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
    
    def run_queries(self):
        return Query.query.join(
            User, (User.id == Query.user_id).order_by(
                Query.timestamp.desc()
            )
        )

class Query(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now())
    query_terms = db.Column(db.String(240))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Query {}>'.format(self.query_terms)

class StoredResults(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    query_id = db.Column(db.Integer, db.ForeignKey('query.id'))
    source = db.Column(db.String(240))
    author = db.Column(db.String(240))
    title = db.Column(db.String(480))
    description = db.Column(db.String(960))
    url = db.Column(db.String(960))
    url_to_image = db.Column(db.String(960))
    published_on = db.Column(db.String(240))
    content = db.Column(db.String(1920))
    SentimentScore = db.Column(db.String(240))
    Compound = db.Column(db.Float)
    Popup = db.Column(db.String(960))
    LocationNames = db.Column(db.String(240))
    Coordinates = db.Column(db.String(120))
    Latitude = db.Column(db.Float)
    Longitude = db.Column(db.Float)
    FrequentWords = db.Column(db.String(480))
    Colors = db.Column(db.String(120))
    Ranking = db.Column(db.Integer)
    
    def __repr__(self):
        return '<Results {}>'.format(self.query_terms)

@login.user_loader
def user_loader(id):
    return User.query.get(int(id))