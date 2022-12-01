from flask import Blueprint, render_template, g, request, redirect, url_for, flash, session, jsonify, current_app
from sqlalchemy import or_

from decorators import login_required
from exts import db
from .forms import JoinForm, ChessForm
from models import ForumModel, AnswerModel, UserModel,Games

bp = Blueprint('play', __name__, url_prefix='/play')


@bp.route('/')
def play():
    return render_template('play.html')
# play page

@bp.route('/chess')
def chess():
    return render_template('chess.html')
# play chess page

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
    current_app.logger.info("Successfully add win or lose")
    return {}
# Store winning and losing information

@bp.route('/chess/range')
def chess_range():
    result = []
    users = UserModel.query.order_by(UserModel.chess_win.desc()).all()
    for user in users:
        result.append({"username": user.username, "chessWin": user.chess_win, "chessLose": user.chess_lose})
    return result
# Ranking information

@bp.route('/game', methods=['GET', 'POST'])
def game():
    form = ChessForm()
    if not session.get("USERNAME") is None:
        if form.validate_on_submit():
            x = int(form.xy.data.split()[0]) + 1
            y = int(form.xy.data.split()[1]) + 1
            win = form.win.data
            user_in_db = UserModel.query.filter(UserModel.username == session.get("USERNAME")).first()
            game_in_db = Games.query.filter(Games.player1 == user_in_db.id).first()
            game_in_db2 = Games.query.filter(Games.player2 == user_in_db.id).first()

            prompt = "You are in a game"
            if game_in_db:
                if (win == "win"):
                    game_in_db.winner = user_in_db.id
                game_in_db.player = game_in_db.player2
                l = list(game_in_db.game)
                l[(x - 1) * 15 + y - 1] = '1'
                game_in_db.game = ''.join(l)
                if (game_in_db.winner == user_in_db.id):
                    prompt = "You win!"
                elif (game_in_db.winner != -1):
                    prompt = "You lost"
                if (game_in_db.winner != -1):
                    db.session.query(Games).filter_by(id=game_in_db.id).delete()
                db.session.commit()
            if game_in_db2:
                if (win == "win"):
                    game_in_db2.winner = user_in_db.id
                game_in_db2.player = game_in_db2.player1
                l = list(game_in_db2.game)
                l[(x - 1) * 15 + y - 1] = '2'
                game_in_db2.game = ''.join(l)
                if (game_in_db2.winner == user_in_db.id):
                    prompt = "You win!"
                elif (game_in_db2.winner != -1):
                    prompt = "You lost"
                if (game_in_db2.winner != -1):
                    db.session.query(Games).filter_by(id=game_in_db2.id).delete()
                db.session.commit()
            flash('X Y:{}'.format(form.xy.data))
            user = {'username': user_in_db.username}
            return redirect('/play/game')
        else:
            user_in_db = UserModel.query.filter(UserModel.username == session.get("USERNAME")).first()
            game_in_db = Games.query.filter(Games.player1 == user_in_db.id).first()
            game_in_db2 = Games.query.filter(Games.player2 == user_in_db.id).first()
            if game_in_db:
                winner = ""
                if (game_in_db.winner == user_in_db.id):
                    winner = "You are the winner!!!"
                g = game_in_db.game
                if (game_in_db.player == user_in_db.id):
                    return render_template('game.html', g=g, winner=winner, form=form, player='1')
                else:
                    return 'Not your turn'
            if game_in_db2:
                winner = ""
                if (game_in_db2.winner == user_in_db.id):
                    winner = "You are the winner!!!"
                g = game_in_db2.game
                if (game_in_db2.player == user_in_db.id):
                    return render_template('game.html', g=g, winner=winner, form=form, player='2')
                else:
                    return 'Not your turn'
            else:
                return redirect('/play/create')
    return redirect('/play')


@bp.route('/create', methods=['GET', 'POST'])
def test():
    form = JoinForm()
    if form.validate_on_submit():
        game = Games(player1=form.player1.data, player2=form.player2.data, player=form.player1.data, game='0' * 256,
                     winner=-1)
        db.session.add(game)
        db.session.commit()
        user_in_db = UserModel.query.filter(UserModel.username == session.get("USERNAME")).first()
        user = {'username': 'Guest'}
        if (user_in_db):
            user = {'username': user_in_db.username}
        return redirect('/play/game')
    user_in_db = UserModel.query.filter(UserModel.username == session.get("USERNAME")).first()
    id = user_in_db.id
    return render_template('join.html', form=form, id=id)
