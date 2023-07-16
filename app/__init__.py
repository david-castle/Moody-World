from config import Config
from flask import Flask
import os


app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config.from_object(Config)


from app import routes, models