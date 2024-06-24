from config import Config
from datetime import datetime
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail, Message
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from logging.handlers import TimedRotatingFileHandler, SMTPHandler
import logging
import os

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config.from_object(Config)
app.config['SECRET_KEY'] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///moody-world-application-tables.db"

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

from app import routes, models, errors

#if not app.debug:
    # Logging to local logs
#    if not os.path.exists('logs'):
#        os.mkdir('logs')
#    logging.basicConfig(filename=f'logs/moodyworld_{datetime.now().strftime("%Y%m%d")}.log', level=logging.INFO, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
#    logger = logging.getLogger()
    #file_handler = TimedRotatingFileHandler(f'logs/moodyworld_{datetime.now().strftime("%Y%m%d")}.log', when='midnight', backupCount=10)
    #file_handler.setFormatter(logging.Formatter(
    #    '%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s [in %(pathname)s:%(lineno)d]'
    #))
    #file_handler.setLevel(logging.INFO)
    #app.logger.addHandler(file_handler)
#    app.logger.setLevel(logging.INFO)
#    app.logger.info("MoodyWorld startup")
    
    # Send logging email 
#    """ if app.config['MAIL_SERVER']:
#        auth = None
#        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
#            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
#        secure = None
#        if app.config['MAIL_USE_TLS']:
#            secure = ()
#        mail_handler = SMTPHandler(
#            mailhost = (app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
#            fromaddr = 'no-reply@' + app.config['MAIL_SERVER'],
#            toaddr = app.config['ADMINS'], subject = 'MoodyWorld Failure Notification',
#            credentials = auth, secure=secure)
#        mail_handler.setLevel(logging.ERROR)
#        app.logger.addHandler(mail_handler) """