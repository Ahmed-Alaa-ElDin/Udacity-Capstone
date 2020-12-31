import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import distinct, func, Date, cast
from datetime import date
from sqlalchemy.orm import relationship
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    db = SQLAlchemy(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://casting:202012@localhost:5432/casting'
    migrate = Migrate(app, db)

    casts = db.Table('casts',
        db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'), primary_key=True),
        db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True)
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

        def __repr__ (self):
            return f'<Artist: {self.id}, {self.name},{self.city},{self.phone},{self.image_link}>'

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

        def __repr__ (self):
            return f'<venue {self.id}, {self.name},{self.city},{self.state},{self.address},{self.phone},{self.image_link},{self.facebook_link}>'

    
    # db.create_all()

    # GO TO HOME PAGE
    @app.route('/', methods=['GET'])
    def home_page():
        return render_template('pages/home.html')
    # GO TO HOME PAGE

    # GO TO MOVIES
    @app.route('/movies', methods=['GET'])
    def show_movies():
        all_movies = Movie.query.all()
        all_actors = dict()
        for movie in all_movies :
            actors = Actor.query.join(casts).join(Movie).filter(casts.c.movie_id == movie.id).all()
            all_actors[movie.id]= actors        
        return render_template('pages/movies.html' , data = all_movies , all_actors = all_actors)
    # GO TO MOVIES

    # CREATE NEW MOVIE
    @app.route('/movies/create', methods=['GET'])
    def create_movie():
        all_actors = Actor.query.all()
        return render_template('pages/new_movie.html',data=all_actors)

    @app.route('/movies/create', methods=['POST'])
    def create_movie_submission():
        error = False

        try:
            name = request.form.get("movie-name")
            date = request.form.get("movie-date")
            city = request.form.get("movie-city")
            genre = request.form.get("movie-genre")
            image = request.form.get("movie-image")
            actors = request.form.getlist("movie-actor")

            new_movie = Movie(title = name, release_date = date, city = city, genre = genre, image_link = image)
            db.session.add(new_movie)
            db.session.commit()

            last_movie = Movie.query.order_by(Movie.id.desc()).first()
            # return json.encode(last_movie)
            for actor in actors:
                actor_data = Actor.query.filter(Actor.id == actor).first()
                actor_data.actors.append(last_movie)
                db.session.commit()

        except:
            error = True
            db.session.rollback()

        finally:
            db.session.close()

        if error:
            abort (400)

        return redirect('/movies')
    # CREATE NEW MOVIE

    # DELETE MOVIE
    @app.route('/movies/delete/<int:movie_id>', methods=['DELETE'])
    def delete_movie(movie_id):
        try:
            item_id = request.get_json()['id']
            movie_delete = Movie.query.get(item_id)
            db.session.delete(movie_delete)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()
    # DELETE MOVIE

    # EDIT ACTOR
    @app.route('/movies/edit/<int:movie_id>', methods=['POST'])
    def edit_movie(movie_id):
        movie_data = Movie.query.filter(Movie.id == movie_id).first()
        
        return render_template('pages/edit_movie.html' , data=movie_data)

    @app.route('/movies/edit/<int:movie_id>', methods=['PATCH'])
    def edit_movie_submission(movie_id):
        title = request.get_json()['title']
        release_date = request.get_json()['release_date']
        city = request.get_json()['city']
        genra = request.get_json()['genra']
        image_link = request.get_json()['image_link']
        
        error = False

        try:
            movie_data = Movie.query.filter(Movie.id == movie_id).first()
            movie_data.title = title
            movie_data.release_date = release_date
            movie_data.city = city
            movie_data.genre = genra
            movie_data.image_link = image_link
            db.session.commit()

        except:
            error = True
            db.session.rollback()

        finally:
            db.session.close()

        if error:
            abort (400)

    # EDIT ACTOR

    # GO TO ACTORS
    @app.route('/actors', methods=['GET'])
    def show_actors():
        all_actors = Actor.query.all()
        return render_template('pages/actors.html' , data=all_actors)
    # GO TO ACTORS

    # CREATE NEW ACTOR
    @app.route('/actors/create', methods=['GET'])
    def create_actor():
        return render_template('pages/new_actor.html')

    @app.route('/actors/create', methods=['POST'])
    def create_actor_submission():
        error = False

        try:
            name = request.form.get("actor-name")
            age = request.form.get("actor-age")
            gender = request.form.get("actor-gender")
            phone = request.form.get("actor-phone")
            genre = request.form.get("actor-genre")
            city = request.form.get("actor-city")
            image = request.form.get("actor-image")
            new_actor = Actor(name = name, age = age, gender = gender, phone = phone, genre = genre, city = city, image_link = image)
            db.session.add(new_actor)
            db.session.commit()

        except:
            error = True
            db.session.rollback()

        finally:
            db.session.close()

        if error:
            abort (400)

        return redirect('/actors')
    # CREATE NEW ACTOR

    # DELETE ACTOR
    @app.route('/actors/delete/<int:actor_id>', methods=['DELETE'])
    def delete_actor(actor_id):
        try:
            item_id = request.get_json()['id']
            actor_delete = Actor.query.get(item_id)
            db.session.delete(actor_delete)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()
    # DELETE ACTOR

    # EDIT ACTOR
    @app.route('/actors/edit/<int:actor_id>', methods=['POST'])
    def edit_actor(actor_id):
        actor_data = Actor.query.filter(Actor.id == actor_id).first()
        db.session.close()
        
        return render_template('pages/edit_actor.html' , data=actor_data)

    @app.route('/actors/edit', methods=['POST'])
    def edit_actor_submission():
        error = False

        try:
            actor_id = request.form.get("actor-id")
            actor_data = Actor.query.filter(Actor.id == actor_id).first()
            actor_data.name = request.form.get("actor-name")
            actor_data.age = request.form.get("actor-age")
            actor_data.gender = request.form.get("actor-gender")
            actor_data.phone = request.form.get("actor-phone")
            actor_data.genre = request.form.get("actor-genre")
            actor_data.city = request.form.get("actor-city")
            actor_data.image_link = request.form.get("actor-image")
            db.session.commit()

        except:
            error = True
            db.session.rollback()

        finally:
            db.session.close()

        if error:
            abort (400)

        return redirect('/actors')

    # EDIT ACTOR
    
    return app