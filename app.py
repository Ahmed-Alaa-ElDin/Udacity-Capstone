import json
import dateutil.parser
from flask import Flask, render_template, request, Response,\
    flash, redirect, url_for, abort, jsonify
from flask_moment import Moment
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import distinct, func, Date, cast
from datetime import date
from sqlalchemy.orm import relationship
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from flask_migrate import Migrate
from models import setup_db, Movie, Actor, casts, db
from authorization import requires_auth


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    migrate = Migrate(app,db)

    # GO TO HOME PAGE
    @app.route('/', methods=['GET'])
    def home_page():
        return render_template('pages/home.html')
    # GO TO HOME PAGE

# ******************************************************
# ======================================================
    # GO TO MOVIES
# ======================================================
    # for API
    @app.route('/api/movies', methods=['GET'])
    @requires_auth("get:movies")
    def show_movies_api(payload):
        all_movies = Movie.query.all()
        all_actors = dict()
        movies_data = [movie.format() for movie in all_movies]
        for movie in all_movies:
            actors = Actor.query.join(casts).join(Movie).\
                filter(casts.c.movie_id == movie.id).all()
            all_actors[movie.id] = actors
        if request.path == "/movies":
            return render_template('pages/movies.html',
                                   data=all_movies, all_actors=all_actors)
        else:
            return jsonify(movies_data)

    # for the web app
    @app.route('/movies', methods=['GET'])
    def show_movies():
        all_movies = Movie.query.all()
        all_actors = dict()
        movies_data = [movie.format() for movie in all_movies]
        for movie in all_movies:
            actors = Actor.query.join(casts).join(Movie).\
                filter(casts.c.movie_id == movie.id).all()
            all_actors[movie.id] = actors
        if request.path == "/movies":
            return render_template('pages/movies.html',
                                   data=all_movies, all_actors=all_actors)
        else:
            return jsonify(movies_data)
    # GO TO MOVIES
# ======================================================

# ======================================================
    # CREATE NEW MOVIE
    @app.route('/movies/create', methods=['GET'])
    def create_movie():
        all_actors = Actor.query.all()
        return render_template('pages/new_movie.html', data=all_actors)

    # for API
    @app.route('/api/movies/create', methods=['POST'])
    @requires_auth("post:movie")
    def create_movie_submission_api(payload):
        error = False

        try:
            movie_id = request.form.get("movie-id")
            name = request.form.get("movie-name")
            date = request.form.get("movie-date")
            city = request.form.get("movie-city")
            genre = request.form.get("movie-genre")
            image = request.form.get("movie-image")
            actors = request.form.getlist("movie-actor")

            if movie_id:
                new_movie = Movie(id=movie_id, title=name, release_date=date,
                                  city=city, genre=genre, image_link=image)
            else:
                new_movie = Movie(title=name, release_date=date, city=city,
                                  genre=genre, image_link=image)

            db.session.add(new_movie)
            db.session.commit()

            last_movie = Movie.query.order_by(Movie.id.desc()).first()

            for actor in actors:
                actor_data = Actor.query.filter(Actor.id == actor).first()
                actor_data.actors.append(last_movie)
                db.session.commit()

        except Exception:
            error = True
            db.session.rollback()

        finally:
            db.session.close()

        if error:
            abort(400)

        if request.path == "/movies/create":
            return redirect('/movies')
        else:
            return f"Movie with name {name} Inserted Successfully"

    # for the web app
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

            new_movie = Movie(title=name, release_date=date, city=city,
                              genre=genre, image_link=image)
            db.session.add(new_movie)
            db.session.commit()

            last_movie = Movie.query.order_by(Movie.id.desc()).first()

            for actor in actors:
                actor_data = Actor.query.filter(Actor.id == actor).first()
                actor_data.actors.append(last_movie)
                db.session.commit()

        except Exception:
            error = True
            db.session.rollback()

        finally:
            db.session.close()

        if error:
            abort(400)

        if request.path == "/movies/create":
            return redirect('/movies')
        else:
            return f"Movie with name {name} Inserted Successfully"
    # CREATE NEW MOVIE
# ======================================================

# ======================================================
    # DELETE MOVIE
    # for API
    @app.route('/api/movies/delete/<int:movie_id>', methods=['DELETE'])
    @requires_auth("delete:movie")
    def delete_movie_api(payload, movie_id):
        error = False
        try:
            movie_delete = Movie.query.get(movie_id)
            db.session.delete(movie_delete)
            db.session.commit()
        except Exception:
            error = True
            db.session.rollback()
        finally:
            db.session.close()

        if error:
            abort(404)
        else:
            return jsonify({
                'status_code': 200,
                'message': 'Movie deleted successfully'
            })

    # for the web app
    @app.route('/movies/delete/<int:movie_id>', methods=['DELETE'])
    def delete_movie(movie_id):
        error = False
        try:
            movie_delete = Movie.query.get(movie_id)
            db.session.delete(movie_delete)
            db.session.commit()
        except Exception:
            error = True
            db.session.rollback()
        finally:
            db.session.close()

        if error:
            abort(404)
        else:
            return jsonify({
                'status_code': 200,
                'message': 'Movie deleted successfully'
            })
    # DELETE MOVIE
# ======================================================

# ======================================================
    # EDIT MOVIE
    # for API
    @app.route('/api/movies/edit/<int:movie_id>', methods=['POST'])
    @requires_auth("patch:movie")
    def edit_movie_api(payload, movie_id):
        movie_data = Movie.query.filter(Movie.id == movie_id).first()

        if request.path.startswith('/movies/edit'):
            return render_template('pages/edit_movie.html', data=movie_data)
        else:
            return f"Welcome to edit page"

    # for the web app
    @app.route('/movies/edit/<int:movie_id>', methods=['POST'])
    def edit_movie(movie_id):
        movie_data = Movie.query.filter(Movie.id == movie_id).first()

        if request.path.startswith('/movies/edit'):
            return render_template('pages/edit_movie.html', data=movie_data)
        else:
            return f"Welcome to edit page"

    # for API
    @app.route('/api/movies/edit/<int:movie_id>', methods=['PATCH'])
    @requires_auth("patch:movie")
    def edit_movie_submission_api(payload, movie_id):
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

        except Exception:
            error = True
            db.session.rollback()

        finally:
            db.session.close()

        if error:
            abort(404)

        if request.path.startswith('/api/movies/edit'):
            return f"Movie edited successfully"

    # for the web app
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

        except Exception:
            error = True
            db.session.rollback()

        finally:
            db.session.close()

        if error:
            abort(404)

        if request.path.startswith('/api/movies/edit'):
            return f"Movie edited successfully"

    # EDIT MOVIE
# ======================================================
# ******************************************************


# ******************************************************
# ======================================================
    # GO TO ACTORS
# ======================================================
    # for API
    @app.route('/api/actors', methods=['GET'])
    @requires_auth("get:actors")
    def show_actors_api(payload):
        all_actors = Actor.query.all()
        actors_data = [actor.format() for actor in all_actors]

        if request.path == "/actors":
            return render_template('pages/actors.html', data=all_actors)
        else:
            return jsonify(actors_data)

    # for the web app
    @app.route('/actors', methods=['GET'])
    def show_actors():
        all_actors = Actor.query.all()
        actors_data = [actor.format() for actor in all_actors]

        if request.path == "/actors":
            return render_template('pages/actors.html', data=all_actors)
        else:
            return jsonify(actors_data)
    # GO TO ACTORS
# ======================================================

# ======================================================
    # CREATE NEW ACTOR
    @app.route('/actors/create', methods=['GET'])
    def create_actor():
        return render_template('pages/new_actor.html')

    # for API
    @app.route('/api/actors/create', methods=['POST'])
    @requires_auth("post:actor")
    def create_actor_submission_api(payload):
        error = False

        try:
            actor_id = request.form.get("actor-id")
            name = request.form.get("actor-name")
            age = request.form.get("actor-age")
            gender = request.form.get("actor-gender")
            phone = request.form.get("actor-phone")
            genre = request.form.get("actor-genre")
            city = request.form.get("actor-city")
            image = request.form.get("actor-image")
            if actor_id:
                new_actor = Actor(id=actor_id, name=name, age=age,
                                  gender=gender, phone=phone, genre=genre,
                                  city=city, image_link=image)
            else:
                new_actor = Actor(name=name, age=age, gender=gender,
                                  phone=phone, genre=genre, city=city,
                                  image_link=image)
            db.session.add(new_actor)
            db.session.commit()

        except Exception:
            error = True
            db.session.rollback()

        finally:
            db.session.close()

        if error:
            abort(400)

        if request.path == "/actors/create":
            return redirect('/actors')
        else:
            return f"Actor with name {name} Inserted Successfully"

    # for the web app
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
            new_actor = Actor(name=name, age=age, gender=gender,
                              phone=phone, genre=genre, city=city,
                              image_link=image)
            db.session.add(new_actor)
            db.session.commit()

        except Exception:
            error = True
            db.session.rollback()

        finally:
            db.session.close()

        if error:
            abort(400)

        if request.path == "/actors/create":
            return redirect('/actors')
        else:
            return f"Actor with name {name} Inserted Successfully"

    # CREATE NEW ACTOR
# ======================================================

# ======================================================
    # DELETE ACTOR
    # for API
    @app.route('/api/actors/delete/<int:actor_id>', methods=['DELETE'])
    @requires_auth("delete:actor")
    def delete_actor_api(payload, actor_id):
        error = False
        try:
            actor_delete = Actor.query.get(actor_id)
            db.session.delete(actor_delete)
            db.session.commit()
        except Exception:
            error = True
            db.session.rollback()
        finally:
            db.session.close()

        if error:
            abort(404)

        else:
            return jsonify({
                'status_code': 200,
                'message': 'Actor deleted successfully'
            })

    @app.route('/actors/delete/<int:actor_id>', methods=['DELETE'])
    def delete_actor(actor_id):
        error = False
        try:
            actor_delete = Actor.query.get(actor_id)
            db.session.delete(actor_delete)
            db.session.commit()
        except Exception:
            error = True
            db.session.rollback()
        finally:
            db.session.close()
        if error:
            abort(404)

        else:
            return jsonify({
                'status_code': 200,
                'message': 'Actor deleted successfully'
            })
    # DELETE ACTOR
# ======================================================

# ======================================================
    # EDIT ACTOR
    # for API
    @app.route('/api/actors/edit/<int:actor_id>', methods=['POST'])
    @requires_auth("patch:actor")
    def edit_actor_api(payload, actor_id):
        actor_data = Actor.query.filter(Actor.id == actor_id).first()
        db.session.close()

        if request.path.startswith('/actors/edit'):
            return render_template('pages/edit_actor.html', data=actor_data)
        else:
            return f"Welcome to edit page"

    # for the web app
    @app.route('/actors/edit/<int:actor_id>', methods=['POST'])
    def edit_actor(actor_id):
        actor_data = Actor.query.filter(Actor.id == actor_id).first()
        db.session.close()

        if request.path.startswith('/actors/edit'):
            return render_template('pages/edit_actor.html', data=actor_data)
        else:
            return f"Welcome to edit page"

    # for API
    @app.route('/api/actors/edit/<int:actor_id>', methods=['PATCH'])
    @requires_auth("patch:actor")
    def edit_actor_submission_api(payload, actor_id):

        name = request.get_json()['name']
        age = request.get_json()['age']
        gender = request.get_json()['gender']
        phone = request.get_json()['phone']
        genre = request.get_json()['genre']
        city = request.get_json()['city']
        image_link = request.get_json()['image']

        error = False

        try:
            actor_data = Actor.query.filter(Actor.id == actor_id).first()
            actor_data.name = name
            actor_data.age = age
            actor_data.gender = gender
            actor_data.phone = phone
            actor_data.genre = genre
            actor_data.city = city
            actor_data.image_link = image_link
            db.session.commit()

        except Exception:
            error = True
            db.session.rollback()

        finally:
            db.session.close()

        if error:
            abort(404)

        if request.path.startswith('/api/actors/edit'):
            return f"Actor edited successfully"

    # for the web app
    @app.route('/actors/edit/<int:actor_id>', methods=['PATCH'])
    def edit_actor_submission(actor_id):

        name = request.get_json()['name']
        age = request.get_json()['age']
        gender = request.get_json()['gender']
        phone = request.get_json()['phone']
        genre = request.get_json()['genre']
        city = request.get_json()['city']
        image_link = request.get_json()['image']

        error = False

        try:
            actor_data = Actor.query.filter(Actor.id == actor_id).first()
            actor_data.name = name
            actor_data.age = age
            actor_data.gender = gender
            actor_data.phone = phone
            actor_data.genre = genre
            actor_data.city = city
            actor_data.image_link = image_link
            db.session.commit()

        except Exception:
            error = True
            db.session.rollback()

        finally:
            db.session.close()

        if error:
            abort(404)

        if request.path.startswith('/api/actors/edit'):
            return f"Actor edited successfully"

    # EDIT ACTOR
# ======================================================
# ******************************************************
    return app
