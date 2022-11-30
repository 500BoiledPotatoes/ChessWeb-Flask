from flask import Flask, jsonify, url_for, redirect, render_template, session, g
from sqlalchemy import column
from flask_migrate import Migrate
from exts import db, mail
from blueprints import user_bp
from blueprints import forum_bp
from blueprints import index_bp
from blueprints import play_bp
from blueprints import book_bp
from models import UserModel
from config import Config
import config

app = Flask(__name__)
app.config.from_object(Config)
app.config.from_object(config)
app.secret_key = "fjhierhgiejgeriojgo"

db.init_app(app)
mail.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(user_bp)
app.register_blueprint(forum_bp)
app.register_blueprint(index_bp)
app.register_blueprint(play_bp)
app.register_blueprint(book_bp)
# Registered blueprint


@app.before_request
def before_request():
    user_id = session.get("user_id")
    if user_id:
        try:
            user = UserModel.query.get(user_id)
            g.user = user
        except:
            g.user = None


@app.context_processor
def context_processor():
    if hasattr(g, "user"):
        return {"user": g.user}
    else:
        return {}


@app.route('/')
def hello_world():  # put application's code here

    engine = db.get_engine()
    with engine.connect() as conn:
        result = conn.execute("select 1")
        print(result.fetchone())

    return 'Hello World!'


if __name__ == '__main__':
    app.run(port=8080)
