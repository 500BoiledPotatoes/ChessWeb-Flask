from flask import Blueprint, render_template, g, request, redirect, url_for, flash, session, jsonify
from sqlalchemy import or_

from decorators import login_required
from exts import db
from .forms import ForumForm, AnswerForm
from models import ForumModel, AnswerModel, UserModel

bp = Blueprint('play', __name__, url_prefix='/play')


@bp.route('/')
def play():
    return render_template('play.html')


@bp.route('/chess')
def chess():
    return render_template('chess.html')


@bp.route('/chess/saveRecord')
@login_required
def chess_save_record():
    user_id = session.get('user_id')
    user = UserModel.query.filter_by(id=user_id).first()
    if request.args.get("flag") == '0':
        user.chess_lose += 1
    else:
        user.chess_win += 1
    db.session.commit()
    return {}


@bp.route('/chess/range')
def chess_range():
    result = []
    users = UserModel.query.order_by(UserModel.chess_win.desc()).all()
    for user in users:
        result.append({"username": user.username, "chessWin": user.chess_win, "chessLose": user.chess_lose})
    return result
