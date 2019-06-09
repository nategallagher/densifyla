import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '8ushyd7978r2jhu89f80jasfjasuydSogfasjhDDgaGsg'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ADDRESS_FOLDER = os.environ.get('ADDRESS_FOLDER') or os.path.abspath("./addresses")
    REPORT_FOLDER = os.environ.get('REPORT_FOLDER') or os.path.abspath("./reports")

    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'localhost'
    MAIL_PORT = os.environ.get('MAIL_PORT') or 3333
    # MAIL_USE_TLS = True
    # MAIL_USERNAME = os.environ.get('MAIL_USER')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASS')

<<<<<<< HEAD
    # MAIL_SUPPRESS_SEND = True  # for now until we get legit mail server
=======
class Production(Config):
	DEBUG = False
	
	SECRET_KEY = b'\t\xcb\xe1\x95\xc9Q\x81(\xfeX\x95\xac,\xc0"Khk\x03\xc3\xed;\xeaI'
	SQLALCHEMY_DATABASE_URI = 'postgresql://densifyla:densifyla@localhost:5432/densifyla'
>>>>>>> origin/v0.0
