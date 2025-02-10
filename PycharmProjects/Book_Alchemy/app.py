from flask import Flask, render_template, session, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book
import os


app = Flask(__name__)
# Ensure the database directory exists
db_path = os.path.abspath("data/library.sqlite")
db_dir = os.path.dirname(db_path)

if not os.path.exists(db_dir):
    os.makedirs(db_dir)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Create the new tables
#with app.app_context():
#    db.create_all()

@app.route('/' ,methods=('GET','POST'))
def home():
    """ This function display the homepage and shows two filters to choice """
    selected_first_filter = request.form.get('first_filter', 'all')
    selected_second_filter = request.form.get('second_filter', '')
    search_title_book = request.form.get('search','')

    # JOIN between Book and Author
    books_authors = db.session.query(Book, Author).join(Author).filter(Book.title.like(f"%{search_title_book}%")).all()
    if request.method == 'POST':
        books_query = ""
        if selected_first_filter == 'books_title':
            books_query = db.session.query(Book.title).join(Author).all()
            if selected_second_filter != '':
                # Query if the book title is the same that it was selected
                books_authors = db.session.query(Book, Author).join(Author) \
                                .filter(Book.title == selected_second_filter).all()
        elif selected_first_filter == 'books_author':
            books_query = db.session.query(Author.name).join(Book).distinct()
            if selected_second_filter != '':
                books_authors = db.session.query(Book, Author).join(Author) \
                                .filter(Author.name == selected_second_filter).all()
        return render_template('home.html',
                                   selected_first_filter=selected_first_filter, books_authors=books_authors,
                                   selected_second_filter=selected_second_filter, books_query=books_query), 201
    return render_template('home.html', books_authors=books_authors,
                           selected_first_filter=selected_first_filter, selected_second_filter=selected_second_filter), 201


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """ This function route to add a new author to the database """
    if request.method == 'POST':
        try:
            #Get anew author from the client
            new_author = Author(
                name = request.form.get('name'),
                birth_date = request.form.get('birthdate'),
                date_of_death = request.form.get('date_of_death')
            )
            db.session.add(new_author)
            db.session.commit()
            message =  f"Author {request.form.get('name')} added successfully!"
            return render_template('add_author.html', message=message), 201
        except ValueError as e:
            message = f"Error: {e}"
            return render_template('add_author.html', message=message), 400
    else:
        return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """ This function add a new book to the database library"""
    authors = db.session.query(Author).all()
    if request.method == 'POST':
        new_book = Book(
            isbn = request.form.get('isbn'),
            title = request.form.get('title'),
            publication_year=int(request.form.get('publication_year')),
            author_id = int(request.form.get('author_id'))
        )
        db.session.add(new_book)
        db.session.commit()
        message = f"Book {request.form.get('title')} added successfully!"
        return render_template('add_book.html', message=message, authors=authors)
    else:
        return render_template('add_book.html', authors=authors)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """ This function delete a book from the database by its ID"""
    # Get book or return 4004 if book_if not found
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    #flash("Book deleted successfully!", "success")
    return render_template('home.html')


@app.route('/list_author', methods=['GET', 'POST'])
def list_authors():
    """ This function retrieve a list of all author or a list of authors to delete"""
    selected_filter = request.form.get("filter", "all_authors")
    authors = db.session.query(Author).all()
    authors_without_books = db.session.query(Author).outerjoin(Book).filter(Book.id.is_(None)).all()
    return render_template('list_author.html', authors_without_books=authors_without_books,
                           authors=authors, selected_filter=selected_filter)


@app.route('/author/<int:author_id>/delete', methods=['POST'])
def delete_author(author_id):
    """ This function delete an author from the database by their ID"""
    authors = db.session.query(Author).all()
    authors_without_books = db.session.query(Author).outerjoin(Book).filter(Book.id.is_(None)).all()
    author = Author.query.get_or_404(author_id)
    for author_book in authors_without_books:
        if author_id == author_book.id:
            db.session.delete(author)
            db.session.commit()
            return render_template('list_author.html', authors=authors)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
