from collections import defaultdict
from db_interactions import DbInteractions


class Actions:
    @classmethod
    def add_new_movie(cls):
        movie_title = input("Enter a movie title: ")
        release_year = str(input("Enter a release year: "))
        result = DbInteractions.add_new_movie(movie_title, release_year)
        print(result)
        return result

    @classmethod
    def view_upcoming_movies(cls):
        upcoming_movies = DbInteractions.view_upcoming_movies()
        print(
            "-" * 30,
            "Following are the upcoming movies:",
            "-" * 30,
            "\n",
        )
        for row in upcoming_movies:
            print(
                "Movie id: ",
                row[0],
                "    Release year: ",
                row[2],
                "    Title: ",
                row[1],
            )
        print("-" * 96)
        return upcoming_movies

    @classmethod
    def view_all_movies(cls):
        all_movies = DbInteractions.view_all_movies()
        print(
            "-" * 30,
            "Following are all the movies:",
            "-" * 30,
            "\n",
        )
        for row in all_movies:
            print(
                "Movie id: ",
                row[0],
                "    Release year: ",
                row[2],
                "    Title: ",
                row[1],
            )
        print("-" * 91)
        return all_movies

    @classmethod
    def set_movie_watched(cls):
        movie_title = input("Enter a title of a movie you watched: ")
        username = input("Enter your username: ")
        message = DbInteractions.set_movie_watched(movie_title, username)
        if message[0] == "Error":
            print(message[1])
        else:
            print(message[1])
        return message[1]

    @classmethod
    def view_watched_movies(cls):
        username = input("Enter your username: ")
        watched_movies = DbInteractions.view_watched_movies(username)
        if watched_movies == []:
            print("\nYou haven't watched any movies yet.")
        elif watched_movies[0] == "Error":
            print(watched_movies[1])
        else:
            print(
                "-" * 10,
                "Following are all the movies you have already watched:",
                "-" * 10,
                "\n",
            )
            for row in watched_movies:
                print(
                    "Movie id: ",
                    row[0],
                    "    Release year: ",
                    row[2],
                    "    Title: ",
                    row[1],
                )
            print("-" * 76)

        return watched_movies

    @classmethod
    def add_new_user(cls):
        username = input("Please provide your username: ")
        message = DbInteractions.add_new_user(username)
        while message[0] == "Error":
            print(message[1])
            username = input(
                "Please provide your username (different than '{}'): ".format(username)
            )
            message = DbInteractions.add_new_user(username)
        print(message[1])
        return message[1]

    @classmethod
    def exit(cls):
        print("Goodbye, and have a nice day!\n")
        return

    @classmethod
    def view_all_users(cls):
        all_records = DbInteractions.view_all_users()
        users_dict = defaultdict(list)
        for username, movie_id, movie_title, release_year in all_records:
            users_dict[username].append([movie_id, movie_title, release_year])
        for key, values in users_dict.items():
            print("Username: ", key, "\nMovies watched: ")
            for value in values:
                if value[0] is None:
                    print("         This user hasn't watched any movies yet!")
                else:
                    print("         ", value)
            print("\n")
