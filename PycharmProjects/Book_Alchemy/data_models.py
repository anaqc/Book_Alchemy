from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


class Author(db.Model):


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    birth_date = db.Column(db.String(20))
    date_of_death = db.Column(db.String(20))


    def __init__(self, name, birth_date, date_of_death=None):
        self.name = name
        self.birth_date = self.validate_date(birth_date)
        self.date_of_death = self.validate_date(date_of_death) if date_of_death else None
        if self.date_of_death and self.date_of_death < self.birth_date:
            raise ValueError("Date of death can not be before birth date")


    @staticmethod
    def validate_date(date_str):
        """
        This function validate date format (YYYY-MM-DD) #
        and convert to datetime object
        """
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid date format. (YYYY-MM-DD)")


    def __str__(self):
        return f"id: {self.id}, name: {self.name}, birth_date: {self.birth_date}, date_of_death: {self.date_of_death}"


class Book(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(50))
    title = db.Column(db.String(50))
    publication_year = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"), nullable=False)


    def __str__(self):
        return (f"id: {self.id}, isbn:{self.isbn}, title: {self.title}, publication_year: {self.publication_year}"
                f", author_id: {self.author_id}")



