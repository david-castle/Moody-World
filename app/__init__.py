from config import Config
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config.from_object(Config)
app.config['SECRET_KEY'] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///moody-world-users.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models