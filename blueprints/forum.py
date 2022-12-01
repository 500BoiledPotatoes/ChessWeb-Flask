from flask import Blueprint, render_template, g, request, redirect, url_for, flash, current_app
from sqlalchemy import or_

from decorators import login_required
from exts import db
from .forms import ForumForm, AnswerForm
from models import ForumModel, AnswerModel

bp = Blueprint("forum", __name__, url_prefix="/forum")


@bp.route("/")
def forum():
    questions = ForumModel.query.order_by(db.text("-create_time")).all()
    return render_template("forum.html", questions=questions)
# Traverse the forum messages based on the creation time


@bp.route("/question", methods=['GET', 'POST'])
@login_required
def post_question():
    if request.method == 'GET':
        return render_template("post_question.html")
    else:
        form = ForumForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            try:
                forum = ForumModel(title=title, content=content, author=g.user)
                db.session.add(forum)
                # Load the post information into the database
                current_app.logger.info("Successfully post")
                db.session.commit()

            except Exception as e:
                current_app.logger.debug("Failed to add post to the database", e)
                db.session.rollback()
            return redirect(url_for("forum.forum"))
        else:
            flash("Formal error")
            return redirect(url_for("forum.post_question"))
# Realize the function of Posting



@bp.route("/question/<int:question_id>")
def question_detail(question_id):
    question = ForumModel.query.get(question_id)
    return render_template("detail.html", question=question)
# See the details of each post


@bp.route("/answer/<int:question_id>",methods=['POST'])
@login_required
def answer(question_id):
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        try:
            answer_model = AnswerModel(content=content,author=g.user,question_id=question_id)
            db.session.add(answer_model)
            # Load the comment information into the database
            db.session.commit()
            current_app.logger.info("Successfully post comment")
        except Exception as e:
            current_app.logger.debug("Failed to add comment to the database", e)
            db.session.rollback()
        return redirect(url_for("forum.question_detail",question_id=question_id))
    else:
        flash("Form validation failed!")
        return redirect(url_for("forum.question_detail", question_id=question_id))
# The ability to comment on posts


@bp.route("/search")
def search():
    q = request.args.get("q")
    questions =ForumModel.query.filter(or_(ForumModel.title.contains(q),ForumModel.content.contains(q))).order_by(db.text("-create_time"))
    return render_template("forum.html", questions=questions)
# Search for posts by keyword



