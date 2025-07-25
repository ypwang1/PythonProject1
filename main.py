from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

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

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movie.db"
db.init_app(app)
Bootstrap5(app)

with app.app_context():
    db.create_all()

# Testing new movie
# with app.app_context():
#
#     db.session.add()
#     db.session.commit()

# CREATE DB


# CREATE TABLE


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == '__main__':

    app.run(debug=True)
