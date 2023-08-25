from flask import Flask, render_template, request, redirect, url_for
from datamanager.json_data_manager import JSONDataManager
from flask_bootstrap import Bootstrap
from forms import UpdateMovieForm, AddUserForm
from imdb_api import search_req
from requests.exceptions import ConnectionError
import os


app = Flask(__name__)
bootstrap = Bootstrap(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
data_manager = JSONDataManager('data/movies.json')  # Use the appropriate path to your JSON file


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>')
def list_user_movies(user_id):
    movies = data_manager.get_user_movies(user_id)
    user_name = data_manager.get_user_name(user_id)

    return render_template('user-movies.html', user_id=user_id, user_name=user_name, movies=movies)


@app.route('/add_user', methods=["GET", "POST"])
def add_user():
    add_form = AddUserForm()
    if request.method == "POST":
        user_name = add_form.user_name.data
        data_manager.add_user(user_name)
        return redirect('/users')

    return render_template('add-user.html', form=add_form)


@app.route('/search_movie/<int:user_id>', methods=["GET", "POST"])
def search_movie(user_id):

    if request.method == "POST":
        title = request.form['title']
        try:
            json_resp = search_req(title)
            if "Search" in json_resp:
                movies = json_resp["Search"]
                results = data_manager.remove_already_favourite(user_id, movies)
                return render_template("search-results.html", user_id=user_id, results=results)
            else:
                return render_template("notfound.html"), 404
        except ConnectionError as e:
            return render_template("notfound.html"), 404

    return render_template('search-movie.html', user_id=user_id)


@app.route('/users/<int:user_id>/add_movie/<imdb_id>', methods=["POST"])
def add_movie(user_id, imdb_id):
    if request.method == "POST":
        data_manager.add_movie(user_id, imdb_id)
        return redirect(url_for('list_user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/update_movie/<imdb_id>', methods=["GET", "POST"])
def update_movie(user_id, imdb_id):
    update_form = UpdateMovieForm()
    if request.method == "POST":
        movies = data_manager.get_user_movies(user_id)
        movie = movies[imdb_id]
        movie['imdb_rating'] = update_form.rating.data
        movie['My_review'] = update_form.review.data
        movies[imdb_id] = movie
        data_manager.write_movies()
        return redirect(url_for('list_user_movies', user_id=user_id))

    movies = data_manager.get_user_movies(user_id)
    movie = movies[imdb_id]
    update_form.rating.data = movie['imdb_rating']
    update_form.review.data = movie['My_review']
    return render_template('update-movie.html', user_id=user_id,
                           imdb_id=imdb_id, movie=movie, form=update_form)


@app.route('/users/<int:user_id>/delete_movie/<imdb_id>', methods=["GET", "POST"])
def delete_movie(user_id, imdb_id):
    if request.method == "POST":
        movies = data_manager.get_user_movies(user_id)
        del movies[imdb_id]
        data_manager.write_movies()
        return redirect(url_for('list_user_movies', user_id=user_id))

    movies = data_manager.get_user_movies(user_id)
    movie = movies[imdb_id]
    return render_template('delete-movie.html', user_id=user_id, imdb_id=imdb_id, movie=movie)


if __name__ == '__main__':
    app.run(debug=True)