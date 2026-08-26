from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
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

@app.route("/books")
def list_books():
    books = db.session.execute(db.select(Book)).scalars()
    return render_template('books.html', books=books)

if __name__ == "__main__":
    app.run(debug=True)