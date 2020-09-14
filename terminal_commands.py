from actions import Actions


class TerminalCommands:
    @classmethod
    def welcome(cls):
        return """Welcome to the watchlist app!"""

    @classmethod
    def select_activity(cls):
        user_input = input(
            """
Please select one of the following options:
1 - Add new movie.
2 - View upcoming movies.
3 - View all movies.
4 - Set a movie as a watched movie.
5 - View watched movies.
6 - Add user to the app.
7 - View all users and movies their watched.
8 - Exit.

Your selection: 
"""
        )
        return cls.activity_execution(user_input)

    @classmethod
    def what_next(cls):
        input("\nPress Enter")
        print("\nWhat do you want to do next?\n")
        return cls.select_activity()

    @classmethod
    def activity_execution(cls, user_input):
        if user_input == "1":
            Actions.add_new_movie()
            return cls.what_next()

        elif user_input == "2":
            Actions.view_upcoming_movies()
            return cls.what_next()

        elif user_input == "3":
            Actions.view_all_movies()
            return cls.what_next()

        elif user_input == "4":
            Actions.set_movie_watched()
            return cls.what_next()

        elif user_input == "5":
            Actions.view_watched_movies()
            return cls.what_next()

        elif user_input == "6":
            Actions.add_new_user()
            return cls.what_next()

        elif user_input == "7":
            Actions.view_all_users()
            return cls.what_next()

        elif user_input == "8":
            Actions.exit()
