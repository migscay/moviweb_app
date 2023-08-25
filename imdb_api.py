import requests
import os
from dotenv import load_dotenv

load_dotenv()

__IMDB_API_KEY__ = os.environ['IMDB_API_KEY']


def search_req(search_query):
    params = {
        "apikey": __IMDB_API_KEY__,
        "s": search_query
    }
    __URL__ = "https://www.omdbapi.com/"
    data = requests.get(__URL__, params=params)
    content = data.json()
    return content


def fetch_data(imdb_id):
    """
    Fetches the movie details via the imdbID
    """
    params = {
        "apikey": __IMDB_API_KEY__,
        "i": imdb_id
    }

    __URL__ = "https://www.omdbapi.com/"
    data = requests.get(__URL__, params=params)
    content = data.json()
    return content
