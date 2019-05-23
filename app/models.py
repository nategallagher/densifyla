from app import app, db
from datetime import datetime


class Address(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    address = db.Column(db.String(140), index=True, nullable=False)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow())

    report_folder = db.Column(db.String(140))
    address_folder = db.Column(db.String(140))

    def __repr__(self):
        return '<Address_{}>'.format(self.address)
