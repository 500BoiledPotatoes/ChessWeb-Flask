from flask import Blueprint, render_template, g, request, redirect, url_for, flash
from sqlalchemy import or_, text

from decorators import login_required
from exts import db
from .forms import ForumForm, AnswerForm
from models import BookModel, AnswerModel

bp = Blueprint('book', __name__, url_prefix="/book")


@bp.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        booktype = request.form["booktype"]
        booktitle = request.form["bookname"]
        publisher = request.form["publisher"]
        year = request.form["year"]
        author = request.form['author']
        try:
            new_book = BookModel(type=booktype, title=booktitle, publisher=publisher, year=year, author=author)
            db.session.add(new_book)
            db.session.commit()
            flash('Successfully added!', 'success')
        except Exception as e:
            print(e)
            flash("Fil to add!", 'danger')
            db.session.rollback()
    return render_template("book_add.html")


@bp.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        booktype = request.form["type"]
        bookname = request.form["name"]
        publisher = request.form["publisher"]
        start_year = request.form["start_year"]
        if (start_year == ''):
            start_year = 0
        end_year = request.form['end_year']
        if (end_year == ''):
            end_year = 99999
        author = request.form['author']
        results = BookModel.query.filter(
            BookModel.type.like('%' + booktype) if booktype is not None else text(""),
            BookModel.title.like('%' + bookname) if bookname is not None else text(""),
            BookModel.publisher.like('%' + publisher) if publisher is not None else text(""),
            BookModel.author.like('%' + author) if author is not None else text(""),
            BookModel.year >= start_year,
            BookModel.year <= end_year,
        ).all()
        if (results):
            return render_template('result.html', results=results)
        else:
            flash('No related books!', 'warning')
            return render_template('search.html')
    return render_template('search.html')

@bp.route('/delete/<int:book_id>', methods=['GET', 'POST'])
def delete(book_id):
    try:
        book = BookModel.query.get(book_id)
        db.session.delete(book)
        db.session.commit()
        flash('Successfully delete')
    except BaseException as e:
        flash('Delete failed')
        db.session.rollback()
        return redirect(url_for('book.search'))
    return redirect(url_for('book.search'))

@bp.route('/deleteAll', methods=['GET', 'POST'])
def deleteAll():
    try:
        if request.method == 'POST':
            books = BookModel.query.all()
            for book in books:
                db.session.delete(book)
        db.session.commit()
        flash('Successfully delete')
    except BaseException as e:
        flash('Delete Failed')
        db.session.rollback()
        return redirect(url_for('book.search'))
    return redirect(url_for('book.search'))
