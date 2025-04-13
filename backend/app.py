from flask import Flask, request
from flask_restful import Api, Resource
from flask_cors import CORS
from flasgger import Swagger, swag_from
import requests, json
from dotenv import load_dotenv
import os
import argparse

#################### Configurations ####################
load_dotenv()
API_KEY = "236e9d003709eb55cf700526b1c268f0"

# Flask app
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app, prefix='/api')

# Swagger
app.config['SWAGGER'] = {
    'title': 'My backend',
    'uiversion': 3,
    'openapi': '3.0.2',
}
swagger = Swagger(app)

MAIN_URL_TMDB: str = "https://api.themoviedb.org/3"
MAIN_URL_QCK: str = "https://quickchart.io/chart"

#################### Helpers ####################

# some useful containers
deleted_movies = set()
liked_movies = set()


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


def getMovieDataWithFilter(main: str, post: str, filters: dict) -> tuple[list, int]:
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


def generateBarPlot(movie_ids: list) -> tuple:
    """
    Generate a bar plot for the given movie IDs
    :param movie_ids: List of movie IDs
    :return: URL of the generated bar plot
    """
    titles = []
    ratings = []
    failed_movie_ids = []

    for movie_id in movie_ids:
        data, status = getDataFromURL(MAIN_URL_TMDB, f"/movie/{movie_id}?api_key={API_KEY}")

        if status != 200:
            failed_movie_ids.append(movie_id)
            continue

        titles.append(data["title"])
        ratings.append(data["vote_average"])

    if not titles:
        return {"error": "No valid movies found"}, 400

    # generate url for the bar plot
    chart_data = {
        "type": "bar",
        "data": {
            "labels": titles,
            "datasets": [{
                "label": "Vote Average",
                "data": ratings,
            }]
        }
    }

    plot_url = f"{MAIN_URL_QCK}?c={chart_data}"

    if failed_movie_ids:
        return {
            "plot_url": plot_url,
            "warning": f"Some movie IDs were invalid: {failed_movie_ids}"
        }, 200

    return {"plot_url": plot_url}, 200


#################### backend Resources ####################

class Movie(Resource):
    @swag_from({
        'responses': {
            200: {
                'description': 'Movie details',
                'content': {
                    'application/json': {
                        'example': {
                            "movie": {
                                "id": 1,
                                "title": "Inception",
                                "overview": "A thief who steals corporate secrets through the use of dream-sharing technology.",
                                "release_date": "2010-07-16"
                            }
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
        """
        Get movie details by ID
        """
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
                'description': 'Movie deleted successfully',
                'content': {
                    'application/json': {
                        'example': {
                            "message": "Movie deleted successfully"
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
                'description': 'ID of the movie to delete',
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
                'description': 'Movie (un)liked successfully',
                'content': {
                    'application/json': {
                        'example': {
                            "message": "Movie (un)liked successfully"
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


class FavouriteMovies(Resource):
    @swag_from({
        'responses': {
            200: {
                'description': 'List of favourite movies',
                'content': {
                    'application/json': {
                        'example': {
                            "movies": [
                                {
                                    "id": 1,
                                    "title": "Inception",
                                    "overview": "A thief who steals corporate secrets through the use of dream-sharing technology.",
                                    "release_date": "2010-07-16"
                                },
                                "..."
                            ]
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
        'tags': ['Favourite'],
    })
    def get(self):
        """
        Get favourite movies
        """
        if not liked_movies:
            return {"error": "No favourite movies found"}, 400

        movies = []
        for movie_id in liked_movies:
            data, status = getDataFromURL(MAIN_URL_TMDB, f"/movie/{movie_id}?api_key={API_KEY}")
            if status == 200:
                movies.append(data)

        return {"movies": movies}


class PopularMovies(Resource):
    @swag_from({
        'responses': {
            200: {
                'description': 'List of popular movies',
                'content': {
                    'application/json': {
                        'example': {
                            "movies": [
                                {
                                    "id": 1,
                                    "title": "Inception",
                                    "overview": "A thief who steals corporate secrets through the use of dream-sharing technology.",
                                    "release_date": "2010-07-16"
                                },
                                "..."
                            ]
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
        """
        Get popular movies
        """
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
    @swag_from({
        'responses': {
            200: {
                'description': 'List of movies with the same genre',
                'content': {
                    'application/json': {
                        'example': {
                            "movies": [
                                {
                                    "id": 1,
                                    "title": "Inception",
                                    "overview": "A thief who steals corporate secrets through the use of dream-sharing technology.",
                                    "release_date": "2010-07-16"
                                },
                                "..."
                            ]
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
        """
        Get movies with the same genre as a given movie
        """
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

    @swag_from({
        'responses': {
            200: {
                'description': 'List of movies with the same runtime',
                'content': {
                    'application/json': {
                        'example': {
                            "movies": [
                                {
                                    "id": 1,
                                    "title": "Inception",
                                    "overview": "A thief who steals corporate secrets through the use of dream-sharing technology.",
                                    "release_date": "2010-07-16"
                                },
                                "..."
                            ]
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
        """
        Get movies with the same runtime as a given movie
        """
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


class BarPlot(Resource):

    @swag_from({
        'responses': {
            200: {
                'description': 'Bar plot URL',
                'content': {
                    'application/json': {
                        'example': {
                            "plot_url": "https://quickchart.io/chart?c={...}"
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
        'tags': ['Bar Plot'],
        'parameters': [
            {
                'name': 'movie_ids',
                'description': 'List of movie IDs to generate bar plot for',
                'in': 'query',
                'type': 'string',
                'required': True
            }
        ],
    })
    def get(self):
        """
        Generate a bar plot for the given movie IDs
        """
        movie_ids_str = request.args.get('movie_ids')

        if not movie_ids_str:
            return {"error": "Movie IDs list cannot be empty"}, 400

        try:
            movie_ids: list = [int(id.strip()) for id in movie_ids_str.split(",")]
        except ValueError:
            return {"error": "Invalid movie IDs format. Ensure they are integers."}, 400

        movie_ids = movie_ids[:10]

        if not movie_ids:
            return {"error": "Movie IDs list cannot be empty"}, 400

        plot_url, status = generateBarPlot(movie_ids)

        if status == 200:
            return {"plot_url": plot_url}
        else:
            return {"error": "Failed to generate bar plot"}, status


#################### Routing ####################

api.add_resource(Movie, '/movies/<int:movie_id>')
api.add_resource(FavouriteMovies, '/movies/favourites')
api.add_resource(PopularMovies, '/movies/popular')
api.add_resource(SameGenreMovies, '/movies/<int:movie_id>/same_genre')
api.add_resource(SameRuntimeMovies, '/movies/<int:movie_id>/same_runtime')
api.add_resource(BarPlot, '/movies/bar_plot')

#################### Main ####################
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Flask API server with API key")
    parser.add_argument('--key', required=True, help="API key for external services (e.g., TMDB)")
    args = parser.parse_args()

    # Save the key to a global or config variable
    API_KEY = args.key

    print(f"Starting server with API key: {API_KEY}")
    app.run(debug=True)
