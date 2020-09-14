import psycopg2
import os
from dotenv import load_dotenv
import datetime

load_dotenv()

class DbInteractions:
    @classmethod
    def select_from_db(cls, query, params=()):
        con = psycopg2.connect(os.environ["DATABASE_URL"])
        with con.cursor() as c:
            c.execute(query, params)
            results = c.fetchall()
            con.close()
            return results

    @classmethod
    def add_to_db(cls, query, params):
        # try:
        con = psycopg2.connect(os.environ["DATABASE_URL"])
        with con.cursor() as c:
            c.execute(query, params)
            con.commit()
            con.close()
            return "\nData added successfully"


    @classmethod
    def create_tables(cls):
        con = psycopg2.connect(os.environ["DATABASE_URL"])
        with con.cursor() as c:
            c.execute(
                """CREATE TABLE IF NOT EXISTS movies (
                    id SERIAL PRIMARY KEY, 
                    movie_title TEXT, 
                    release_year INTEGER
                    )"""
            )
            c.execute(
                """CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY
                    )"""
            )
            c.execute(
                """CREATE TABLE IF NOT EXISTS watched (
                    movie_id INTEGER,
                    username TEXT,
                    FOREIGN KEY (movie_id) REFERENCES movies (id),
                    FOREIGN KEY (username) REFERENCES users (username)
                    )"""
            )
            con.commit()
            con.close()

    @classmethod
    def add_new_movie(cls, movie_title, release_year):
        query = "INSERT INTO movies (movie_title, release_year) VALUES (%s, %s)"
        params = (movie_title, release_year)
        return cls.add_to_db(query, params)

    @classmethod
    def view_upcoming_movies(cls):
        current_year = int(datetime.datetime.now().strftime("%Y"))
        query = """
        SELECT * FROM movies
        WHERE release_year > (%s)
        ORDER BY release_year"""
        params = (current_year,)
        results = cls.select_from_db(query, params)
        return results

    @classmethod
    def view_all_movies(cls):
        query = "SELECT * FROM movies ORDER BY release_year"
        results = cls.select_from_db(query)
        return results

    @classmethod
    def set_movie_watched(cls, movie_title, username):
        check_title = "SELECT id FROM movies WHERE movie_title = %s"
        params = (movie_title,)
        movie_id = cls.select_from_db(check_title, params)
        check_username = "SELECT username FROM users WHERE username = %s"
        params = (username,)
        user_exists = cls.select_from_db(check_username, params)
        if movie_id and user_exists:
            params = (movie_id[0][0], username)
            query = "INSERT INTO watched VALUES (%s, %s)"
            communication = cls.add_to_db(query, params)
            message = ["message", communication]

        elif not movie_id and not user_exists:
            message = [
                "Error",
                "It looks like you don't have an account yet. Please create one using option 6. Also, the movie you indicated is not in the db yet, you need to add it first to our database using option 1.",
            ]

        elif not movie_id:
            message = [
                "Error",
                "We don't have this move in our database. Please double check the title you've provided. If the movie is not in the db, you need to add it first - use option 1 for that).",
            ]

        elif not user_exists:
            message = [
                "Error",
                "We don't have this username in our database. Please double check the username you've provided. If you don't have an account, you can create one using option 6).",
            ]
        else:
            message = ["Kurwa", "Cos nie dziala"]

        return message

    @classmethod
    def view_watched_movies(cls, username):
        query = """
        SELECT username FROM users
        WHERE username = %s"""
        params = (username,)
        user = cls.select_from_db(query, params)
        if user:
            query = """
            SELECT * FROM movies 
            JOIN watched ON movie_id = movies.id
            JOIN users ON users.username = watched.username
            WHERE watched.username = %s
            ORDER BY movies.release_year
            """
            params = (username,)
            results = cls.select_from_db(query, params)
        else:
            results = ["Error", "\nNo user found with this username. Please double check the username you've entered. If you don't have an account yet, create one using option 6."]

        return results

    @classmethod
    def add_new_user(cls, username):
        check_user = """
        SELECT username FROM users 
        WHERE username = (%s)"""
        params = (username,)
        existing_user = cls.select_from_db(check_user, params)
        if existing_user:
            message = [
                "Error",
                "Sorry, but a user with a username '{}' already exists. Please choose another username.".format(
                    username
                ),
            ]
            return message

        query = """
        INSERT INTO users
        VALUES (%s)"""

        communication = cls.add_to_db(query, params)
        message = ["Message", communication]

        return message

    @classmethod
    def view_all_users(cls):
        query = """
        SELECT users.username, movies.* FROM users
        LEFT JOIN watched ON watched.username = users.username
        LEFT JOIN movies ON watched.movie_id = movies.id
        """
        results = cls.select_from_db(query)
        return results
