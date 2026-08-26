import os

from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from wtforms import IntegerField, SubmitField, StringField
from wtforms.validators import DataRequired
import requests
from dotenv import load_dotenv

load_dotenv()

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
Bootstrap5(app)
db.init_app(app)
movies = []

class EditMovieForm(FlaskForm):
    rating = IntegerField("Your Rating out of 10", validators=[DataRequired()])
    review = StringField("Your Review", validators=[DataRequired()])
    button = SubmitField("Done")

class AddMovieForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    button = SubmitField("Add Movie")

# CREATE DB
class Movie(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    year: Mapped[int]
    description: Mapped[str]
    rating: Mapped[float]
    review: Mapped[str]
    img_url: Mapped[str]
# CREATE TABLE
with app.app_context():
    db.create_all()
    first_movie = db.session.execute(db.select(Movie)).first()
    if not first_movie:
        first_movie = Movie(
            title="Phone Booth",
            year=2002,
            description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
            rating=7.3,
            review="My favourite character was the caller.",
            img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
        )
        second_movie = Movie(
            title="Avatar The Way of Water",
            year=2022,
            description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
            rating=7.5,
            review="I liked the water.",
            img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
        )
        db.session.add(first_movie)
        db.session.add(second_movie)
        db.session.commit()

@app.route("/")
def home():
    movies = db.session.execute(db.select(Movie).order_by(Movie.rating)).scalars().all()
    return render_template("index.html", movies=movies)

@app.route("/edit/<movie_id>", methods=["GET", "POST"])
def edit(movie_id):
    if request.method == "GET":
        form = EditMovieForm()
        return render_template("edit.html", form=form)
    elif request.method == "POST":
        rating = request.form["rating"]
        review = request.form["review"]
        movie = db.get_or_404(Movie, movie_id)
        movie.rating = float(rating)
        movie.review = review
        db.session.commit()
        return redirect("/")
    else:
        return redirect("/")

@app.route("/delete/<movie_id>")
def delete(movie_id):
    movie = db.get_or_404(Movie, movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect("/")

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        form = AddMovieForm()
        return render_template("add.html", form=form)
    elif request.method == "POST":
        title=request.form["title"]
        movie_data_response = requests.get(url='https://api.themoviedb.org/3/search/movie', params={
            'query': title
        }, headers={
            'Authorization': 'Bearer ' + os.getenv('BEARER_TOKEN')
        })
        movie_data = movie_data_response.json()
        global movies
        movies = movie_data["results"]
        return render_template("select.html", movies=movies)
    else:
        return redirect("/")

@app.route("/select/<movie_index>")
def select(movie_index):
    movie = movies[int(movie_index)]
    title = movie["title"]
    year = movie["release_date"][:4]
    description = movie["overview"]
    rating = movie["vote_average"]
    review = ""
    img_url = f"https://image.tmdb.org/t/p/original{movie['poster_path']}"
    new_movie = Movie(
        title=title,
        year=year,
        description=description,
        rating=rating,
        review=review,
        img_url=img_url
    )
    db.session.add(new_movie)
    db.session.commit()
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
