from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

import os
import logging
from logging.handlers import RotatingFileHandler


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
mail = Mail(app)
migrate = Migrate(app, db)
login = LoginManager(app)

app.jinja_env.globals['enumerate'] = enumerate

if not os.path.exists(app.config['ADDRESS_FOLDER']):
    os.mkdir(app.config['ADDRESS_FOLDER'])

if not os.path.exists(app.config['REPORT_FOLDER']):
    os.mkdir(app.config['REPORT_FOLDER'])

from app import routes, models

if not app.debug:
    if not os.path.exists('logs/'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/densifyla.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('DensifyLA startup')
