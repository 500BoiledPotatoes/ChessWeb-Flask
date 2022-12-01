from flask import Blueprint, render_template, g, request, redirect, url_for, flash, session, logging, current_app
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
        #Gets the value passed from the front end
        try:
            new_book = BookModel(type=booktype, title=booktitle, publisher=publisher, year=year, author=author)
            db.session.add(new_book)
            db.session.commit()
            flash('Successfully added!', 'success')
            current_app.logger.info("Add book successfully")
        except Exception as e:
            flash("Fil to add!", 'danger')
            current_app.logger.debug("Failed to add data to the database", e)
            db.session.rollback()
    return render_template("book_add.html")
# Add a book to the database

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
        # Gets the value passed from the front end
        results = BookModel.query.filter(
            BookModel.type.like('%' + booktype) if booktype is not None else text(""),
            BookModel.title.like('%' + bookname) if bookname is not None else text(""),
            BookModel.publisher.like('%' + publisher) if publisher is not None else text(""),
            BookModel.author.like('%' + author) if author is not None else text(""),
            BookModel.year >= start_year,
            BookModel.year <= end_year,
        ).all()
        current_app.logger.info("Search book successfully")
        #Fuzzy query
        if (results):
            return render_template('result.html', results=results)
        else:
            flash('No related books!', 'warning')
            return render_template('search.html')
    return render_template('search.html')
#Search related books


@bp.route('/delete/<int:book_id>', methods=['GET', 'POST'])
def delete(book_id):
    try:
        book = BookModel.query.get(book_id)
        db.session.delete(book)
        db.session.commit()
        flash('Successfully delete')
        current_app.logger.info("Successfully delete")
    except BaseException as e:
        flash('Delete failed')
        current_app.logger.debug("Database deletion failed",e)
        db.session.rollback()
        return redirect(url_for('book.search'))
    return redirect(url_for('book.search'))
#Delete a single book
@bp.route('/deleteAll', methods=['GET', 'POST'])
def deleteAll():
    if 'user_id' in session and session['user_id']== 1:
        print(session['user_id'])
        try:
            if request.method == 'POST':
                books = BookModel.query.all()
                for book in books:
                    db.session.delete(book)
            db.session.commit()
            flash('Successfully delete')
            current_app.logger.info("Successfully delete")
        except BaseException as e:
            flash('Delete Failed')
            current_app.logger.debug("Database delete all data failed", e)
            db.session.rollback()
            return redirect(url_for('book.search'))
    else:
        flash("You are not Administrator")

    return redirect(url_for('book.search'))
# Delete all books
