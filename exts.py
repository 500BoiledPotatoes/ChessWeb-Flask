from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from log import Logger

db = SQLAlchemy()
mail = Mail()
logger = Logger()