import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from config import SQLALCHEMY_DATABASE_URI


db = SQLAlchemy()


def setup_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    db.app = app
    db.init_app(app)
    db.create_all()


casts = db.Table('casts',
                 db.Column('actor_id', db.Integer,
                           db.ForeignKey('actor.id'), primary_key=True),
                 db.Column('movie_id', db.Integer,
                           db.ForeignKey('movie.id'), primary_key=True)
                 )


class Actor (db.Model):
    __tablename__ = 'actor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    age = db.Column(db.Integer)
    gender = db.Column(db.Integer)
    city = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genre = db.Column(db.String())
    image_link = db.Column(db.String(500))

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'city': self.city,
            'phone': self.phone,
            'genre': self.genre,
            'image_link': self.image_link
        }

    def __repr__(self):
        return f'<Artist: {self.id}, {self.name},{self.city}\
            ,{self.phone},{self.image_link}>'


class Movie(db.Model):
    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    release_date = db.Column(db.Date)
    city = db.Column(db.String(120))
    genre = db.Column(db.String())
    image_link = db.Column(db.String(500))
    actors = db.relationship('Actor', secondary=casts,
                             backref=db.backref('actors', lazy='dynamic'))

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'city': self.city,
            'genre': self.genre,
            'image_link': self.image_link,
        }

    def __repr__(self):
        return f'<venue {self.id}, {self.name},{self.city},\
            {self.state},{self.address},{self.phone},{self.image_link}\
                ,{self.facebook_link}>'


# db.create_all()
