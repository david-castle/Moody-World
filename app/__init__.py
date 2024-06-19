from config import Config
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail, Message
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from logging.handlers import RotatingFileHandler
import logging
import os

#logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config.from_object(Config)
app.config['SECRET_KEY'] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///moody-world-users.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
mail = Mail(app)

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'contact@example.com'
app.config["MAIL_PASSWORD"] = 'your-password'
mail.init_app(app)

from app import routes, models

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/moodyworld.log', backupCount=10, maxBytes=10240)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("MoodyWorld startup")