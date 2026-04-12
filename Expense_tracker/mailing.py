from flask import Blueprint, render_template
from flask_mail import Mail, Message

mailing_bp = Blueprint('mailing',__name__)

def send_email():
    mailing_bp.config['MAIL_SERVER'] = 'smtp.gmail.com'
    mailing_bp.config['MAIL_PORT'] = 587
    mailing_bp.config['MAIL_USE_TLS'] = True
    mailing_bp.config['MAIL_USERNAME'] = 'ashwathr27100@gmail.com'
    mailing_bp.config['MAIL_PASSWORD'] = 'uzpg hgap bcfh hwki'  # NOT your Gmail password
    mailing_bp.config['MAIL_DEFAULT_SENDER'] = 'ashwathr27100@gmail.com'

    mail = Mail(mailing_bp)
    return mail