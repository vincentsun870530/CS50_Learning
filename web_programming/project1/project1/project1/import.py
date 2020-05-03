import csv
import os

from flask import Flask
from werkzeug.security import generate_password_hash
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


def main():
    # add an admin user
    user = User(email="admin@admin.com", password=generate_password_hash("admin"), name="admin")
    db.session.add(user)
    f = open("books.csv")
    reader = csv.reader(f)
    next(reader, None)
    # print(reader)
    for col1, col2, col3, col4 in reader:
        # SQL
        # db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
        #            {"isbn":col1, "title": col2, "author": col3, "year": col4})
        # print(f"Add book isbn {col1} title {col2} author {col3} year {col4}.")
        # db.commit()
        # ORM
        book = Book(isbn=col1, title=col2, author=col3, year=col4)
        db.session.add(book)
        print(f"Add book isbn {col1} title {col2} author {col3} year {col4}.")
    db.session.commit()


if __name__ == "__main__":
    # need this line to run as python program
    with app.app_context():
        main()
