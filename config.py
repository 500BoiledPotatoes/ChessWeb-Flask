# HOSTNAME = '127.0.0.1'
# PORT = '3306'
# DATABASE = 'chess_web'
# USERNAME = 'root'
# PASSWORD = 'cc20020330'
# DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
# SQLALCHEMY_DATABASE_URI = DB_URI
# SQLALCHEMY_TRACK_MODIFICATIONS = True

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Lu Jingyu 20205767'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'chessweb.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
# Connect to the sqlite database

MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_DEBUG = True
MAIL_USERNAME = "344482899@qq.com"
MAIL_PASSWORD = "ebkflhviwvsecbcj"
MAIL_DEFAULT_SENDER = "344482899@qq.com"
# Connecting the Mailbox platform

