from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler
from flask_bootstrap import Bootstrap
from flask_mail import Mail


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)
mail = Mail(app)

login = LoginManager(app)
login.login_view = 'login'


## FOR SENDING ERRORS VIA MAILS
if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']), 
                fromaddr='noreply@' + app.config['MAIL_SERVER'],
                toadds=app.config['ADMINS'], subject='Basic App failure',
                credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


from app import routes, models, errors
