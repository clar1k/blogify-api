import smtplib
from config.config import Config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from itsdangerous import URLSafeSerializer

s = URLSafeSerializer(Config.SECRET_KEY)


def send_message(email: str, token: str) -> bool:
    with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
        msg = MIMEMultipart()
        
        msg['From'] = "TestieMan4ik"
        msg['To'] = email
        msg['Subject'] = "Confirm your account :D"
        
        msg.attach(MIMEText(f"Your link is http://127.0.0.1:8000/confirm/{token}",'plain'))
        
        server.starttls()
        server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
        server.send_message(msg)
        return True


def generate_confirm_token(email: str):
    return s.dumps(email, Config.SECRET_KEY)


def get_email_by_token(token):
    return s.loads(token, Config.SECRET_KEY)