from flask import Blueprint, render_template

bp = Blueprint("personal", __name__, url_prefix="/personal")


@bp.route("/")
def personalspace():
    return render_template("personalspace.html")