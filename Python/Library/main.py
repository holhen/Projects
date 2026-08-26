from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books-collection.db"
# initialize the app with the extension
db.init_app(app)

class Book(db.Model):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

with app.app_context():
    db.create_all()
    books = db.session.execute(db.select(Book)).first()
    if not books:
        book = Book(
            id=1,
            title="Harry Potter",
            author="J. K. Rowling",
            rating=9.8
        )
        db.session.add(book)
        db.session.commit()

@app.route("/")
@app.route("/index.html")
def list_books():
    books = db.session.execute(db.select(Book)).scalars().all()
    return render_template('index.html', books=books)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        rating = request.form["rating"]
        book = Book(
            title=title,
            author=author,
            rating=rating
        )
        db.session.add(book)
        db.session.commit()
        return redirect('/')
    return render_template("add.html")

@app.route("/edit/<book_id>", methods=["GET", "POST"])
def edit(book_id):
    if request.method == "GET":
        book = db.get_or_404(Book, book_id)
        return render_template("edit_rating.html", book=book)
    elif request.method == "POST":
        new_rating = request.form["rating"]
        book = db.get_or_404(Book, book_id)
        book.rating = float(new_rating)
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/')

@app.route("/delete/<book_id>")
def delete(book_id):
    book = db.get_or_404(Book, book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect('/')



if __name__ == "__main__":
    app.run(debug=True)