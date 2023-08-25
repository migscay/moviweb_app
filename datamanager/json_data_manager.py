import json
from .data_manager_interface import DataManagerInterface
from imdb_api import fetch_data


class JSONDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename
        self.movies = self.read_movies()

    def read_movies(self):
        with open(self.filename, "r") as movies_json:
            return json.load(movies_json)

    def write_movies(self):
        with open(self.filename, "w") as movies_json:
            json.dump(self.movies, movies_json)

    def get_all_users(self):
        # Return all users
        users = []
        for key, value in self.movies.items():
            user = {'id': key, 'name': value['name'], 'movies': value['movies']}
            users.append(user)

        return users

    def get_user_movies(self, user_id):
        """
        Return all the movies for a given user

        :param user_id:
        :return: dictionary of movies
        """
        return self.movies[str(user_id)]["movies"]

    def get_user_name(self, user_id):
        """
        :param user_id:
        :return: user_name
        """
        return self.movies[str(user_id)]["name"]

    def add_user(self, user_name):
        """
        add a new user
        :param user_name:
        :return:
        """
        if len(self.movies.keys()) == 0:
            last_user_id = 0
        else:
            last_user_id = int(max(self.movies.keys()))

        print(last_user_id)

        user_detail = {'name': user_name, 'movies': {}}
        last_user_id += 1
        self.movies[last_user_id] = user_detail
        self.write_movies()
        self.movies = self.read_movies()
        print(self.movies)

    def add_movie(self, user_id, imdb_id):
        """
        add movie to user movies
        :param user_id:
        :param imdb_id:
        :return:
        """
        movies = self.get_user_movies(user_id)
        if imdb_id in movies:
            print(f"Movie {imdb_id} already exist!")
            return

        movie_data = fetch_data(imdb_id)
        movie_details = {'Title': movie_data['Title'],
                         'Genre': movie_data['Genre'],
                         'My_review': "",
                         'Year': movie_data['Year'],
                         'Director': movie_data['Director'],
                         'imdb_rating': movie_data['imdbRating'],
                         'img_url': movie_data['Poster']}
        movies[imdb_id] = movie_details
        self.movies[str(user_id)]["movies"] = movies
        self.write_movies()

    def remove_already_favourite(self, user_id, movies):
        """
        removes movies already in user favourites
        :param user_id:
        :param movies: search results for adding movie
        :return:
        """
        favourites = self.get_user_movies(user_id)
        not_yet_favourites = [movie for movie in movies if not favourites.get(movie['imdbID'])]
        return not_yet_favourites
