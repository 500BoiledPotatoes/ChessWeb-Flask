from flask import Flask, jsonify, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from exts import db
from blueprints import user_bp
from blueprints import forum_bp


import config

app = Flask(__name__)
app.config.from_object(config)

app.register_blueprint(user_bp)
app.register_blueprint(forum_bp)

db.init_app(app)


@app.route('/')
def hello_world():  # put application's code here

    engine = db.get_engine()
    with engine.connect()  as conn:
        result = conn.execute("select 1")
        print(result.fetchone())

    return 'Hello World!'


if __name__ == '__main__':
    app.run()


