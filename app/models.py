from app import app, db, login
from datetime import datetime
from flask_login import UserMixin
import jwt
from jwt import InvalidSignatureError, ExpiredSignatureError
import time
from werkzeug.security import generate_password_hash, check_password_hash


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Address(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    address = db.Column(db.String(140), nullable=False)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow())

    report_folder = db.Column(db.String(140), unique=True)
    address_folder = db.Column(db.String(140))

    def __repr__(self):
        return '<Address_{}>'.format(self.address)


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(140), index=True, unique=True)
    email_confirmed = db.Column(db.Boolean, default=False)

    password_hash = db.Column(db.String(128))

    # relationships
    address = db.relationship('Address', backref='user', lazy='dynamic')

    def __repr__(self):
        return "<User_{}>".format(self.id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_password_reset_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time.time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256'
        ).decode('utf-8')

    @staticmethod
    def verify_password_reset_token(token):
        try:
            user_id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except ExpiredSignatureError:
            return
        except InvalidSignatureError:
            return
        return User().query.get(user_id)

    def get_email_confirmation_token(self):
        return jwt.encode(
            {'confirm_email': self.id},
            app.config['SECRET_KEY'], algorithm='HS256'
        ).decode('utf-8')

    @staticmethod
    def verify_email_confirmation_token(token):
        try:
            user_id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['confirm_email']
        except ExpiredSignatureError:
            return
        except InvalidSignatureError:
            return
        return User().query.get(user_id)
