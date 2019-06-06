from app import mail
from threading import Thread


def send_email(app, msg):
    """
    Send email with application context
    Args:
         app: current app
         msg: message object, e.g. flask_mail.Message
    """
    with app.app_context():
        mail.send(msg)


def send_mail_thread(app, msg):
    Thread(target=send_email, args=(app, msg)).start()
