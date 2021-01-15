import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from flask import jsonify
from models import setup_db, Movie, Actor, casts, db
from config import tokens


db = SQLAlchemy()


def setup_db(app, database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class CastingTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = 'postgresql://casting:202012@localhost:5432/\
            casting_test'
        setup_db(self.app, self.database_path)

        self.new_movie_one = {
            'movie-id': '50',
            'movie-name': 'Mohammed PBUH',
            'movie-date': '2021-01-02',
            'movie-city': 'Mecca',
            'movie-genre': 'Islamic',
            'movie-image': 'www.google.com',
        }

        self.new_movie_two = {
            'movie-id': '51',
            'movie-name': 'Mohammed PBUH',
            'movie-date': '2021-01-02',
            'movie-city': 'Mecca',
            'movie-genre': 'Islamic',
            'movie-image': 'www.google.com',
        }

        self.edit_movie = {
            'title': 'Mohammed PBUH',
            'release_date': '2019-01-02',
            'city': 'Mecca',
            'genra': 'Islamic',
            'image_link': 'www.facebook.com',
        }

        self.new_actor_one = {
            'actor-id': '50',
            'actor-name': 'Ali',
            'actor-age': 60,
            'actor-gender': 1,
            'actor-phone': '01111335648',
            'actor-genre': 'Scientific',
            'actor-city': 'Cairo',
            'actor-image': 'www.google.com'
        }

        self.new_actor_two = {
            'actor-id': '51',
            'actor-name': 'Ali',
            'actor-age': 60,
            'actor-gender': 1,
            'actor-phone': '01111335648',
            'actor-genre': 'Scientific',
            'actor-city': 'Cairo',
            'actor-image': 'www.google.com'
        }

        self.edit_actor = {
            'name': 'Hala Hassan',
            'age': 20,
            'gender': 2,
            'phone': '01111339306',
            'genre': 'Scientific',
            'city': 'Cairo',
            'image': 'www.google.com'
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

# test home page end points
    def test_home_page_success(self):
        res = self.client().get("/")
        self.assertEqual(res.status_code, 200)

    def test_home_page_fail(self):
        res = self.client().get("/1")
        self.assertEqual(res.status_code, 404)

# test movies page
    def test_show_movies_success(self):
        res = self.client().get("/api/movies",
                                headers={'Authorization':
                                         tokens['executive_producer']})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data))

    def test_create_new_movie_template_success(self):
        res = self.client().get("/movies/create")
        self.assertEqual(res.status_code, 200)

    def test_create_movie_submission_success(self):
        res = self.client().post("api/movies/create", data=self.new_movie_one,
                                 headers={'Authorization':
                                          tokens['executive_producer']})
        res = self.client().post("api/movies/create", data=self.new_movie_two,
                                 headers={'Authorization':
                                          tokens['executive_producer']})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, b'Movie with name Mohammed PBUH Inserted\
             Successfully')

    def test_create_movie_submission_fail(self):
        res = self.client().post("api/movies/create",
                                 data={"movie-date": "Ahmed"},
                                 headers={'Authorization':
                                          tokens['executive_producer']})

        self.assertEqual(res.status_code, 400)

    def test_delete_movie_success(self):
        res = self.client().delete("/api/movies/delete/51",
                                   headers={'Authorization':
                                            tokens['executive_producer']})
        data = json.loads(res.data)

        self.assertEqual(data['status_code'], 200)
        self.assertEqual(data['message'], 'Movie deleted successfully')

    def test_delete_movie_fail(self):
        res = self.client().delete("/api/movies/delete/1000",
                                   headers={'Authorization':
                                            tokens['executive_producer']})
        data = json.loads(res.data)

        self.assertEqual(data['status_code'], 404)
        self.assertEqual(data['message'], 'Movie isn\'t found')

    def test_edit_movie_template_success(self):
        last_movie = Movie.query.order_by(Movie.id.desc()).first()

        res = self.client().post("/api/movies/edit/51",
                                 headers={'Authorization':
                                          tokens['executive_producer']})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, b'Welcome to edit page')

    def test_edit_movie_template_fail(self):
        res = self.client().get("/api/movies/edit/",
                                headers={'Authorization':
                                         tokens['executive_producer']})
        self.assertEqual(res.status_code, 404)

    def test_edit_movie_submission_success(self):
        last_movie = Movie.query.order_by(Movie.id.desc()).first()

        res = self.client().patch("/api/movies/edit/" + str(last_movie.id),
                                  json=self.edit_movie,
                                  content_type='application/json',
                                  headers={'Authorization':
                                           tokens['executive_producer']})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, b'Movie edited successfully')

    def test_edit_movie_submission_fail(self):
        res = self.client().patch("/api/movies/edit/",
                                  headers={'Authorization':
                                           tokens['executive_producer']})

        self.assertEqual(res.status_code, 404)

# test actors page
    def test_show_actors_success(self):
        res = self.client().get("/api/actors",
                                headers={'Authorization':
                                         tokens['executive_producer']})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data))

    def test_create_new_actor_template_success(self):
        res = self.client().get("/actors/create")
        self.assertEqual(res.status_code, 200)

    def test_create_actor_submission_success(self):
        res = self.client().post("api/actors/create",
                                 data=self.new_actor_one,
                                 headers={'Authorization':
                                          tokens['executive_producer']})
        res = self.client().post("api/actors/create",
                                 data=self.new_actor_two,
                                 headers={'Authorization':
                                          tokens['executive_producer']})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, b'Actor with name Ali Inserted\
                         Successfully')

    def test_create_actor_submission_fail(self):
        res = self.client().post("api/actors/create",
                                 data={"actor-gender": "Ahmed"},
                                 headers={'Authorization':
                                          tokens['executive_producer']})

        self.assertEqual(res.status_code, 400)

    def test_delete_actor_success(self):
        last_actor = Actor.query.order_by(Actor.id.desc()).first()

        res = self.client().delete("/api/actors/delete/51",
                                   headers={'Authorization':
                                            tokens['executive_producer']})
        data = json.loads(res.data)

        self.assertEqual(data['status_code'], 200)
        self.assertEqual(data['message'], 'Actor deleted successfully')

    def test_delete_actor_fail(self):
        res = self.client().delete("/api/actors/delete/1000",
                                   headers={'Authorization':
                                            tokens['executive_producer']})
        data = json.loads(res.data)

        self.assertEqual(data['status_code'], 404)
        self.assertEqual(data['message'], 'Actor isn\'t found')

    def test_edit_actor_template_success(self):
        last_actor = Actor.query.order_by(Actor.id.desc()).first()

        res = self.client().post("/api/actors/edit/" + str(last_actor.id),
                                 headers={'Authorization':
                                          tokens['executive_producer']})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, b'Welcome to edit page')

    def test_edit_actor_template_fail(self):
        res = self.client().get("/api/actors/edit/",
                                headers={'Authorization':
                                         tokens['executive_producer']})
        self.assertEqual(res.status_code, 404)

    def test_edit_actor_submission_success(self):

        res = self.client().patch("/api/actors/edit/50",
                                  json=self.edit_actor,
                                  content_type='application/json',
                                  headers={'Authorization':
                                           tokens['executive_producer']})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, b'Actor edited successfully')

    def test_edit_actor_submission_fail(self):
        res = self.client().post("/api/movies/edit/",
                                 headers={'Authorization':
                                          tokens['executive_producer']})

        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main()
