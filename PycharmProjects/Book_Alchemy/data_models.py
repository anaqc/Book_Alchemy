from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Author(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    birth_date = db.Column(db.String(10))
    date_of_death = db.Column(db.String(10))


    def __str__(self):
        return f"id: {self.id}, name: {self.name}, birth_date: {self.birth_date}, date_of_death: {self.date_of_death}"


class Book(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(50))
    title = db.Column(db.String(50))
    publication_year = db.Column(db.String(10))
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"), nullable=False)


    def __str__(self):
        return (f"id: {self.id}, isbn:{self.isbn}, title: {self.title}, publication_year: {self.publication_year}"
                f", author_id: {self.author_id}")



