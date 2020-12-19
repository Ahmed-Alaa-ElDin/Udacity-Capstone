import json
# import dateutil.parser
# import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import distinct, func, Date, cast
from datetime import date
from sqlalchemy.orm import relationship
# import logging
# from logging import Formatter, FileHandler
# from flask_wtf import Form
from flask_migrate import Migrate

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://casting:202012@localhost:5432/casting'
migrate = Migrate(app, db)

class Actors (db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    age = db.Column(db.Integer)
    gender = db.Column(db.Integer)
    city = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genre = db.Column(db.String())
    image_link = db.Column(db.String(500))
    def __repr__ (self):
        return f'<Artist: {self.id}, {self.name},{self.city},{self.phone},{self.image_link}>'

class Movie(db.Model):
    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    release_date = db.Column(db.Date) 
    city = db.Column(db.String(120))
    genre = db.Column(db.String())
    def __repr__ (self):
        return f'<venue {self.id}, {self.name},{self.city},{self.state},{self.address},{self.phone},{self.image_link},{self.facebook_link}>'

db.create_all()

@app.route('/', methods=['GET'])
def enter_home_page():
    return render_template('pages/home.html')

if __name__ == '__main__':
    app.run()