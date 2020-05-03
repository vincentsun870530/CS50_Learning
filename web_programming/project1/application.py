import os

# Import flask method 1, flask 2. global variable, 3. redirect page, 4. url, 5. session, 6. flash pop up
from flask import Flask, g, redirect, url_for, session, flash, render_template, jsonify, request
# Import two method 1. generate hash, 2. check hash
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Session
app.secret_key = 'somesecretkeythatonlyishouldknow'


@app.before_request
def before_request():
    g.user = None


@app.route("/")
def index():
    if not g.user:
        return redirect(url_for('login'))
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    g.user = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        app.logger.info(email)
        app.logger.info(password)
        # Check email is existed or not
        db_user = User.query.filter_by(email=email).first()
        # app.logger.info(db_user.email)
        # app.logger.info(db_user.password)
        # result = check_password_hash(db_user.password, password)
        # app.logger.info(result)
        if db_user is None or not check_password_hash(db_user.password, password):
            flash("This is wrong username or password")
            return redirect(url_for('login'))
        g.user = db_user
        return render_template("index.html", user=db_user)
    return render_template("login.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        # Clean previous session
        session.pop('user_id', None)

        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        name = request.form['name']
        # app.logger.info(check_password_hash(password, request.form['re-password']))
        # Check password and re-enter password are the same
        if not check_password_hash(password, request.form['re-password']):
            flash("Please confirm password you entered is same", "error")
            return redirect(url_for('register'))
        # app.logger.info(email, password, name)

        # Check email is existed or not
        db_user = User.query.filter_by(email=email).first()
        if db_user is not None:
            flash("This email is existed", "error")
            return redirect(url_for('register'))

        # Connect to db and insert user
        user = User(email=email, password=password, name=name)
        db.session.add(user)
        db.session.flush()

        # At this point, the object user has been pushed to the DB,
        # and has been automatically assigned a unique primary key id
        app.logger.info(user.id)
        session['user_id'] = user.id

        db.session.commit()
        flash("Successful registered", "info")
        return redirect(url_for('login'))

    return render_template("register.html")


@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/search", methods=["GET"])
def search():
    isbn = request.args.get("isbn")
    title = request.args.get('title')
    author = request.args.get("author")
    # app.logger.info(title)
    books = Book.query.filter(or_(Book.title == title, Book.isbn == isbn, Book.author == author)).all()
    # app.logger.info(book[0].title)
    if len(books) == 0:
        return render_template("error.html", message="No such book")

    # Get search result
    return render_template("result.html", books=books)


@app.route("/book/<int:book_id>")
def book(book_id):
    book = Book.query.get(book_id)
    return render_template("book.html", book=book)
