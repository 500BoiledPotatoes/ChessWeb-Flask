from flask import Blueprint,render_template

bp = Blueprint("forum", __name__, url_prefix="/")

@bp.route("/forum")
def forum():
    return render_template("index.html")