from flask import Flask, render_template, session, request,jsonify
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book
import os


app = Flask(__name__)
# Ensure the database directory exists
db_path = os.path.abspath("datas/library.sqlite")
db_dir = os.path.dirname(db_path)

if not os.path.exists(db_dir):
    os.makedirs(db_dir)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
#books = session.query(Book).all()
#authors = session.query(Author).all()
#restaurants = session.query(Restaurant).all()
# Create the new tables
#with app.app_context():
#    db.create_all()

@app.route('/' ,methods=('GET','POST'))
def home():
    selected_first_filter = request.form.get('first_filter', 'all')
    selected_second_filter = request.form.get('second_filter', '')
    # Perform an explicit JOIN between Book and Author
    books_authors = db.session.query(Book, Author).join(Author).all()
    if request.method == 'POST':
        books_option = ""
        if selected_first_filter == 'books_title':
            books_option = db.session.query(Book.id, Book.title).join(Author).all()
        elif selected_first_filter == 'books_author':
            books_option = db.session.query(Author.id, Author.name).all()
        return render_template('home.html',
                                   selected_first_filter=selected_first_filter, books_authors=books_authors,
                                   selected_second_filter=selected_second_filter, books_option=books_option), 201
    return render_template('home.html', books_authors=books_authors,
                           selected_first_filter=selected_first_filter, selected_second_filter=selected_second_filter), 201


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        #Get anew author from the client
        new_author = Author(
            name = request.form.get('name'),
            birth_date = request.form.get('birthdate'),
            date_of_death = request.form.get('date_of_death')
        )
        db.session.add(new_author)
        db.session.commit()
        return jsonify({"Message": "Author added successfully!"}), 201
    else:
        return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        new_book = Book(
            isbn = request.form.get('isbn'),
            title = request.form.get('title'),
            publication_year=int(request.form.get('publication_year')),
            author_id = int(request.form.get('author_id'))
        )
        db.session.add(new_book)
        db.session.commit()
        return jsonify({"Message":"Book added successfully!"}), 201
    else:
        return render_template('add_book.html')

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
