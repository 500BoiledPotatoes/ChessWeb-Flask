from flask import Blueprint, render_template

bp = Blueprint("play", __name__, url_prefix="/play")


@bp.route("/")
def play():
    return render_template("play.html")
