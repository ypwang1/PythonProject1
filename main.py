from crypt import methods
from pydoc import describe

from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import os
from dotenv import load_dotenv

load_dotenv()

KEY = os.getenv("KEY")
API_URL =  "http://www.omdbapi.com/"

# CREATE DB
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Movie(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    year: Mapped[int] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    rating:Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(nullable=True)
    review: Mapped[str] = mapped_column(String(1000), nullable=True)
    img_url: Mapped[str] = mapped_column(String(200), nullable=True)

class RateMovieForm(FlaskForm):
    rating = StringField("Your Rating Out of 10 e.g. 7.5")
    review = StringField("Your review")
    submit = SubmitField("Done")

class AddNewMovie(FlaskForm):
    new_movie_title = StringField('Movie Title')
    submit = SubmitField('Add movie')

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movie.db"
db.init_app(app)
Bootstrap5(app)


# CREATE TABLE
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    result = db.session.execute(db.select(Movie).order_by(Movie.rating))
    all_movies = result.scalars()
    return render_template("index.html", movies = all_movies)

@app.route("/edit/<int:index>", methods=['POST', 'GET'])
def edit(index):
    form = RateMovieForm()
    movie = db.session.get(Movie, index)
    if form.validate_on_submit():
        movie.rating = form.rating.data
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', movie = movie, form=form)

@app.route("/<int:index>")
def delete(index):
    movie = db.session.get(Movie, index)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/add', methods=['POST', 'GET'])
def add():
    form = AddNewMovie()
    if form.validate_on_submit():
        title = form.new_movie_title.data
        params = {
            "apikey": KEY,
            "s": title
        }
        response = requests.get(url=API_URL, params=params)
        movies = response.json()
        return render_template('select.html', movies=movies['Search'])
    return render_template('add.html', form=form)

@app.route('/add/<string:index>')
def find_movie(index):
    params = {
        "apikey": KEY,
        "i": index
    }
    response = requests.get(url=API_URL, params=params)
    movie = response.json()
    ratings = movie.get('Ratings')
    if ratings and len(ratings) > 0 and 'Value' in ratings[0]:
        rating_value = float(movie['Ratings'][0]['Value'].split('/')[0])
    else:
        rating_value = 0.0
    new_movie = Movie(title=movie['Title'], year=int(movie['Year']), description=movie['Plot'], rating=rating_value, img_url=movie['Poster'])
    db.session.add(new_movie)
    db.session.commit()
    the_movie = db.session.execute(db.select(Movie).where(Movie.title == movie['Title'])).scalar()
    movie_id = the_movie.id
    return redirect(url_for('edit', index=movie_id))

if __name__ == '__main__':

    app.run(debug=True)
