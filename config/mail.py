from os import environ as env
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from itsdangerous import URLSafeSerializer
s = URLSafeSerializer('secret_key')

load_dotenv('.env')
class MailConfig():
    SMTP_SERVER = env.get('MAIL_SERVER')
    SMTP_PORT = env.get('MAIL_PORT')
    MAIL_USERNAME = env.get('MAIL_USERNAME')
    MAIL_PASSWORD = env.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = env.get('MAIL_DEFAULT_SENDER')


def send_message(recipient: str, token: str) -> bool:
    with smtplib.SMTP(MailConfig.SMTP_SERVER, MailConfig.SMTP_PORT) as server:
        msg = MIMEMultipart()
        
        msg['From'] = "TestieMan4ik"
        msg['To'] = recipient
        msg['Subject'] = "Confirm your account :D"
        
        msg.attach(MIMEText(f"Your link is http://127.0.0.1:8000/confirm/{token}",'plain'))
        
        server.starttls()
        server.login(MailConfig.MAIL_USERNAME, MailConfig.MAIL_PASSWORD)
        server.send_message(msg)
        return True


def generate_confirm_token(email: str):
    return s.dumps(email, 'secret_key')


def get_email_by_token(token):
    return s.loads(token, 'secret_key')