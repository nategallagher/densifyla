from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Production

import os

app = Flask(__name__)
app.config.from_object(Production)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

if not os.path.exists(app.config['ADDRESS_FOLDER']):
    os.mkdir(app.config['ADDRESS_FOLDER'])

if not os.path.exists(app.config['REPORT_FOLDER']):
    os.mkdir(app.config['REPORT_FOLDER'])

from app import routes, models
