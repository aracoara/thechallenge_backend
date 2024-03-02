# tennis_app/__init__.py
from flask import Flask
import logging
from tennis_app.extensions import db, migrate, login_manager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
import os
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect   

# Configuração do logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
# app.config['WTF_CSRF_TIME_LIMIT'] = 3600  # Por exemplo, 1 hora
# csrf = CSRFProtect(app)

CORS(app, supports_credentials=True, origins="*")
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,X-Requested-With')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
    response.headers.add('Access-Control-Expose-Headers', 'Content-Type,Authorization,X-Requested-With,Access-Control-Allow-Origin')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smash_picks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bcrypt = Bcrypt(app)

## Configuração para usar o MailHog
# app.config['MAIL_SERVER'] = 'localhost'
# app.config['MAIL_PORT'] = 1025
# app.config['MAIL_USE_TLS'] = False  # MailHog não usa TLS
# app.config['MAIL_USE_SSL'] = False  # MailHog não usa SSL
# # Não é necessário MAIL_USERNAME ou MAIL_PASSWORD com MailHog
# app.config['MAIL_USERNAME'] = None
# app.config['MAIL_PASSWORD'] = None
# # Configuração opcional do remetente padrão
# app.config['MAIL_DEFAULT_SENDER'] = 'guilherme.solino@gmail.com'  # Substitua pelo e-mail desejado

## Configuração do Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')


mail = Mail(app)

db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    from tennis_app.models import User
    return User.query.get(int(user_id))

from tennis_app import models
from tennis_app import routes
