import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app

def setup_db(app, database_path):
    db = SQLAlchemy()
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

class CastingTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = 'postgresql://casting:202012@localhost:5432/casting_test'
        setup_db(self.app, self.database_path)
        
        self.new_movie = {
            'title' : 'Mohammed PBUH',
            'release_date' : '20-01-2020',
            'city' : 'Mecca',
            'genre' : 'Islamic',
            'image_link' : 'www.google.com'
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    def test_home_page (self):
        res = self.client().get("/")

        self.assertEqual(res.status_code , 200)

    def test_show_movies (self):
        res = self.client().get("/movies")
        self.assert_template_used('pages/movies.html')
        self.assertEqual(res.status_code , 200)

        # data = res.get('data')
        # print(data["all_actors"])
        # self.assertEqual(res.status_code , 200)
        # self.assertEqual(data['success'], True)
        # self.assertTrue(data['all_movies'])
        # self.assertTrue(len(data['all_movies']))



if __name__ == "__main__":
    unittest.main()