from flask import Flask, request
from flask_restful import Api, Resource
from flask_cors import CORS
from flasgger import Swagger, swag_from
import requests, json
from dotenv import load_dotenv
import os

#################### Configurations ####################
load_dotenv()
API_KEY = "236e9d003709eb55cf700526b1c268f0" if os.getenv("API_KEY") is None else os.getenv("API_KEY")

# Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
api = Api(app, prefix='/api')

# Swagger
app.config['SWAGGER'] = {
    'title': 'My API',
    'uiversion': 3,
    'openapi': '3.0.2',
}
swagger = Swagger(app)

MAIN_URL_TMDB: str = "https://api.themoviedb.org/3"
MAIN_URL_QCK: str = "https://quickcharts.io/chart"

#################### Helpers ####################

# some containers
deleted_movies = set()
liked_movies = set()

def get_api_key():
    """
    Get API key from environment variables
    """
    if 'API_KEY' not in os.environ:
        raise ValueError("API_KEY not found in environment variables")
    return os.environ['API_KEY']

def getFilters(filters: list) -> dict:
    """
    List of filters that are applicable
    :param filters: List of filters to apply (e.g., genre, amount, etc.)
    :return: Dictionary of filters
    """
    filter_dict = {}
    for filter in filters:
        if filter == "amount":
            filter_dict['amount'] = filters[filter]

    return filter_dict


def getDataFromURL(main: str, post: str = "") -> tuple:
    """
    Fetch data from the given URL. If you know it's returning JSON, you can use this function.
    """
    url = f"{main}{post}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json(), response.status_code
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None, 500

def getMovieDataWithFilter(main:str, post:str, filters: dict) -> tuple[list, int]:
    """
    Get movies with the given filters
    :param main: Main URL
    :param post: Endpoint URL
    :param filters: List of filters to apply (e.g., amount, genre, etc.)
    :return: List of movies
    """

    amount = filters.get('amount', 5)
    page = filters.get('page', 1)
    genre = filters.get('genre', [])
    runtime = filters.get('runtime', 0)
    runtime_diff = filters.get('runtime_diff', 0)

    movies = []

    while len(movies) < amount:
        # Construct the URL with filters
        url = f"{main}{post}?api_key={API_KEY}&page={page}"

        if genre:
            url += f"&with_genres={",".join(str(g) for g in genre)}"

        if runtime > 0:
            url += f"&with_runtime.gte={runtime - runtime_diff}&with_runtime.lte={runtime + runtime_diff}"

        data, status = getDataFromURL(url)

        if status != 200:
            return [], status

        movies.extend(data.get("results", []))
        page += 1

    return movies[:amount], 200


#################### API Resources ####################

class Movie(Resource):
    """
    Get movie details by ID
    """
    @swag_from({
        'responses': {
            200: {
                'description': 'Movie details',
                'examples': {
                    'application/json': {
                        "movie": {
                            "id": 1,
                            "title": "Inception",
                            "overview": "A thief who steals corporate secrets through the use of dream-sharing technology.",
                            "release_date": "2010-07-16"
                        }
                    }
                }
            },
            400: {
                'description': 'Bad Request'
            },
            500: {
                'description': 'Internal Server Error'
            }
        },
        'tags': ['Movie'],
        'parameters': [
            {
                'name': 'movie_id',
                'description': 'ID of the movie to fetch',
                'in': 'path',
                'type': 'integer',
                'required': True
            }
        ],
    })
    def get(self, movie_id):
        if not isinstance(movie_id, int):
            return {"error": "Invalid movie ID"}, 400

        if movie_id <= 0:
            return {"error": "Movie ID must be a positive integer"}, 400

        data, status = getDataFromURL(MAIN_URL_TMDB, f"/movie/{movie_id}?api_key={API_KEY}")
        if status == 200:
            return {"movie": data}
        else:
            return {"error": "Failed to fetch movie details"}

    @swag_from({
        'responses': {
            204: {
                'description': 'Movie liked successfully',
                'examples': {
                    'application/json': {
                        "message": "Movie liked successfully"
                    }
                }
            },
            400: {
                'description': 'Bad Request'
            },
            500: {
                'description': 'Internal Server Error'
            }
        },
        'tags': ['Movie'],
        'parameters': [
            {
                'name': 'movie_id',
                'description': 'ID of the movie to like',
                'in': 'path',
                'type': 'integer',
                'required': True
            }
        ],
    })
    def delete(self, movie_id):
        """
        Delete a movie by ID
        """
        if not isinstance(movie_id, int):
            return {"error": "Invalid movie ID"}, 400

        if movie_id <= 0:
            return {"error": "Movie ID must be a positive integer"}, 400

        if movie_id in deleted_movies:
            return {"error": "Movie already deleted"}, 400

        deleted_movies.add(movie_id)
        return {"message": f"Movie with ID {movie_id} deleted successfully"}, 204

    @swag_from({
        'responses': {
            201: {
                'description': 'Movie liked/unliked successfully',
                'examples': {
                    'application/json': {
                        "message": "Movie liked successfully"
                    }
                }
            },
            400: {
                'description': 'Bad Request'
            },
            500: {
                'description': 'Internal Server Error'
            }
        },
        'tags': ['Movie'],
        'parameters': [
            {
                'name': 'movie_id',
                'description': 'ID of the movie to like/unlike',
                'in': 'path',
                'type': 'integer',
                'required': True
            }
        ],
    })
    def put(self, movie_id):
        """
        Like/unlike a movie by ID
        """
        if not isinstance(movie_id, int):
            return {"error": "Invalid movie ID"}, 400

        if movie_id <= 0:
            return {"error": "Movie ID must be a positive integer"}, 400

        if movie_id in liked_movies:
            liked_movies.remove(movie_id)
            return {"message": f"Movie with ID {movie_id} unliked successfully"}, 201
        else:
            liked_movies.add(movie_id)
            return {"message": f"Movie with ID {movie_id} liked successfully"}, 201


class PopularMovies(Resource):
    """
    Get popular movies
    """
    @swag_from({
        'responses': {
            200: {
                'description': 'List of popular movies',
                'examples': {
                    'application/json': {
                        "movies": [
                            {
                                "id": 1,
                                "title": "Inception",
                                "overview": "A thief who steals corporate secrets through the use of dream-sharing technology.",
                                "release_date": "2010-07-16"
                            }
                        ]
                    }
                }
            },
            400: {
                'description': 'Bad Request'
            },
            500: {
                'description': 'Internal Server Error'
            }
        },
        'tags': ['Popular'],
        'parameters': [
            {
                'name': 'amount',
                'description': 'Number of popular movies to fetch',
                'in': 'query',
                'type': 'integer',
                'required': False,
                'default': 5
            }
        ],
    })
    def get(self):
        n_popular_movies: int = request.args.get('amount', default=5, type=int)

        if not isinstance(n_popular_movies, int):
            return {"error": "Invalid amount"}, 400

        if n_popular_movies <= 0:
            return {"error": "Amount must be a positive integer"}, 400

        if n_popular_movies > 20:
            return {"error": "Amount must be less than or equal to 20"}, 400

        filters: dict = {
            "amount": n_popular_movies,
        }

        movies, status = getMovieDataWithFilter(MAIN_URL_TMDB, "/movie/popular", filters)

        if status == 200:
            return {"movies": movies}
        else:
            return {"error": "Failed to fetch popular movies"}, status

class SameGenreMovies(Resource):
    """
    Get movies with the same genre as a given movie
    """
    @swag_from({
        'responses': {
            200: {
                'description': 'List of movies with the same genre',
                'examples': {
                    'application/json': {
                        "movies": [
                            {
                                "id": 1,
                                "title": "Inception",
                                "overview": "A thief who steals corporate secrets through the use of dream-sharing technology.",
                                "release_date": "2010-07-16"
                            }
                        ]
                    }
                }
            },
            400: {
                'description': 'Bad Request'
            },
            500: {
                'description': 'Internal Server Error'
            }
        },
        'tags': ['Same Genre'],
        'parameters': [
            {
                'name': 'movie_id',
                'description': 'ID of the movie to fetch similar movies for',
                'in': 'path',
                'type': 'integer',
                'required': True
            },
            {
                'name': 'amount',
                'description': 'Number of similar movies to fetch',
                'in': 'query',
                'type': 'integer',
                'required': False,
                'default': 5
            }
        ],
    })
    def get(self, movie_id):

        n_movies: int = request.args.get('amount', default=5, type=int)

        if not isinstance(movie_id, int) or not isinstance(n_movies, int):
            return {"error": "Invalid movie ID or amount"}, 400

        if movie_id <= 0 or n_movies <= 0:
            return {"error": "Movie ID must be a positive integer and amount must be a positive integer"}, 400

        if n_movies > 20:
            return {"error": "Amount must be less than or equal to 20"}, 400

        movie, status = getDataFromURL(MAIN_URL_TMDB, f"/movie/{movie_id}?api_key={API_KEY}")

        if status != 200:
            return {"error": "Failed to fetch movie details"}, status

        if "genres" not in movie:
            return {"error": "No genres found for this movie"}, 400

        filters = {
            "amount": n_movies,
            "genre": [genre['id'] for genre in movie["genres"]]
        }

        movies, status = getMovieDataWithFilter(MAIN_URL_TMDB, "/discover/movie", filters)

        if status == 200:
            return {"movies": movies}
        else:
            return {"error": "Failed to fetch movies with the same genre"}, status


class SameRuntimeMovies(Resource):
    """
    Get movies with the same runtime as a given movie
    """
    @swag_from({
        'responses': {
            200: {
                'description': 'List of movies with the same runtime',
                'examples': {
                    'application/json': {
                        "movies": [
                            {
                                "id": 1,
                                "title": "Inception",
                                "overview": "A thief who steals corporate secrets through the use of dream-sharing technology.",
                                "release_date": "2010-07-16"
                            }
                        ]
                    }
                }
            },
            400: {
                'description': 'Bad Request'
            },
            500: {
                'description': 'Internal Server Error'
            }
        },
        'tags': ['Same Runtime'],
        'parameters': [
            {
                'name': 'movie_id',
                'description': 'ID of the movie to fetch similar movies for',
                'in': 'path',
                'type': 'integer',
                'required': True
            },
            {
                'name': 'amount',
                'description': 'Number of similar movies to fetch',
                'in': 'query',
                'type': 'integer',
                'required': False,
                'default': 5
            },
            {
                'name': 'runtime_diff',
                'description': 'Allowed difference in runtime (in minutes)',
                'in': 'query',
                'type': 'integer',
                'required': False,
                'default': 5
            }
        ],
    })
    def get(self, movie_id):
        n_movies: int = request.args.get('amount', default=5, type=int)
        runtime_diff = request.args.get('runtime_diff', default=5, type=int)

        if not isinstance(movie_id, int) or not isinstance(n_movies, int) or not isinstance(runtime_diff, int):
            return {"error": "Invalid movie ID, amount or runtime_diff"}, 400

        if movie_id <= 0 or n_movies <= 0 or runtime_diff <= 0:
            return {"error": "Movie ID, amount and runtime_diff must be positive integers"}, 400

        if n_movies > 20:
            return {"error": "Amount must be less than or equal to 20"}, 400

        if runtime_diff > 10:
            return {"error": "Runtime difference must be less than or equal to 10"}, 400

        movie, status = getDataFromURL(MAIN_URL_TMDB, f"/movie/{movie_id}?api_key={API_KEY}")

        if status != 200:
            return {"error": "Failed to fetch movie details"}, status

        if "runtime" not in movie:
            return {"error": "No runtime found for this movie"}, 400

        filters = {
            "amount": n_movies,
            "runtime": movie["runtime"],
            "runtime_diff": 10
        }

        movies, status = getMovieDataWithFilter(MAIN_URL_TMDB, "/discover/movie", filters)

        if status == 200:
            return {"movies": movies}
        else:
            return {"error": "Failed to fetch movies with the same runtime"}, status


#################### Routing ####################

api.add_resource(Movie, '/movies/<int:movie_id>')
api.add_resource(PopularMovies, '/movies/popular')
api.add_resource(SameGenreMovies, '/movies/<int:movie_id>/same_genre')
api.add_resource(SameRuntimeMovies, '/movies/<int:movie_id>/same_runtime')


#################### Main ####################
if __name__ == '__main__':
    app.run(debug=True)
