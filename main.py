from crypt import methods

from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests


# CREATE DB
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Movie(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    year: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    rating:Mapped[float] = mapped_column(Float, nullable=False)
    ranking: Mapped[int] = mapped_column(nullable=False)
    review: Mapped[str] = mapped_column(String(1000), nullable=False)
    img_url: Mapped[str] = mapped_column(String(200), nullable=False)

class RateMovieForm(FlaskForm):
    rating = StringField("Your Rating Out of 10 e.g. 7.5")
    review = StringField("Your review")
    submit = SubmitField("Done")


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movie.db"
db.init_app(app)
Bootstrap5(app)


# CREATE TABLE
with app.app_context():
    db.create_all()

# Testing new movie
# with app.app_context():
#
#     db.session.add()
#     db.session.commit()

@app.route("/")
def home():
    result = db.session.execute(db.select(Movie).order_by(Movie.id))
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

@app.route('/add')
def add():
    new_movie= Movie(

    )
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':

    app.run(debug=True)
