from os import environ as env
from dotenv import load_dotenv

if not load_dotenv('.env'):
    raise Exception('Could not find dotenv file in root directory')


class Config:
    SECRET_KEY = env.get('SECRET_KEY')
    SMTP_SERVER = env.get('MAIL_SERVER') 
    SMTP_PORT = env.get('MAIL_PORT')
    MAIL_USERNAME = env.get('MAIL_USERNAME')
    MAIL_PASSWORD = env.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = env.get('MAIL_DEFAULT_SENDER')
    MONGO_CONNECTION = env.get('MONGO_CONNECTION')
    UPLOAD_FOLDER = env.get('UPLOAD_FOLDER')