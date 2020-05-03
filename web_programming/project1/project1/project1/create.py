import os

from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


def main():
    # Delete all the table
    db.drop_all()
    print("Successful dropped")
    # Create new tables
    db.create_all()
    print("Successful created")


if __name__ == "__main__":
    with app.app_context():
        main()
