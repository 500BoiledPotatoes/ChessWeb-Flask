from flask import Blueprint, render_template, g, request, redirect, url_for, flash
from decorators import login_required
from exts import db
from .forms import ForumForm, AnswerForm
from models import ForumModel, AnswerModel

bp = Blueprint("forum", __name__, url_prefix="/forum")


@bp.route("/")
def forum():
    questions = ForumModel.query.order_by(db.text("-create_time")).all()
    return render_template("forum.html", questions=questions)


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
            forum = ForumModel(title=title, content=content, author=g.user)
            db.session.add(forum)
            db.session.commit()
            return redirect("/")
        else:
            flash("Formal error")
            return redirect(url_for("forum.post_question"))


@bp.route("/question/<int:question_id>")
def question_detail(question_id):
    question = ForumModel.query.get(question_id)
    return render_template("detail.html", question=question)


@bp.route("/answer/<int:question_id>",methods=['POST'])
@login_required
def answer(question_id):
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        answer_model = AnswerModel(content=content,author=g.user,question_id=question_id)
        db.session.add(answer_model)
        db.session.commit()
        return redirect(url_for("forum.question_detail",question_id=question_id))
    else:
        flash("表单验证失败！")
        return redirect(url_for("forum.question_detail", question_id=question_id))

