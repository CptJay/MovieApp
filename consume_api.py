import requests

BASE_URL = "http://localhost:5000/api/"

def popularMovies(amount: int = 5):
    print("This code tests the popular movies endpoint.")
    response = requests.get(BASE_URL + "movies/popular", params={"amount": amount})
    if response.status_code == 200:
        movies = response.json()
        print(f"Popular Movies (first {amount}):")
        for movie in movies["movies"]:
            print(f"\t {movie['title']} (ID: {movie['id']})")
    else:
        print("Failed to fetch popular movies:", response.status_code, response.text)


def sameGenreMovies(movie_id: int = 5, amount: int = 5):
    print("This code tests the same genre movies endpoint.")
    response = requests.get(BASE_URL + f"movies/{movie_id}/same_genre", params={"amount": amount})
    if response.status_code == 200:
        movies = response.json()
        print(f"Movies with the same genre as movie ID {movie_id} (first {amount}):")
        for movie in movies["movies"]:
            print(f"\t {movie['title']} (ID: {movie['id']})")
            print(f"\t\t -> Genre: {[f"{id2}" for id2 in movie['genre_ids']]}")
    else:
        print("Failed to fetch same genre movies:", response.status_code, response.text)

def similarRuntimeMovies(movie_id: int = 5, amount: int = 5):
    print("This code tests the similar runtime movies endpoint.")
    response = requests.get(BASE_URL + f"movies/{movie_id}/same_runtime", params={"amount": amount})
    if response.status_code == 200:
        movies = response.json()
        print(f"Movies with a similar runtime to movie ID {movie_id} (first {amount}):")
        for movie in movies["movies"]:
            print(f"\t {movie['title']} (ID: {movie['id']})")
    else:
        print("Failed to fetch similar runtime movies:", response.status_code, response.text)

def plotBarMovies(movie_ids: list = [5, 6, 7]):
    print("This code tests the plot bar movies endpoint.")
    response = requests.get(BASE_URL + "movies/bar_plot", params={"movie_ids": ",".join([str(id2) for id2 in movie_ids])})
    if response.status_code == 200:
        movies = response.json()
        print("URL: ", movies["plot_url"])
    else:
        print("Failed to fetch plot bar movies:", response.status_code, response.text)

def favoriteMovie(movie_id: int = 5):
    print("This code tests the (un)favorite movie endpoint.")
    response = requests.put(BASE_URL + f"movies/{movie_id}")
    if response.status_code == 201:
        movies = response.json()
        print(f"Movie ID {movie_id} has been (un)favorited.")
    else:
        print("Failed to favorite movie:", response.status_code, response.text)

def getFavorites():
    print("This code tests the get all favorite movies endpoint.")
    response = requests.get(BASE_URL + "movies/favourites")
    if response.status_code == 200:
        movies = response.json()
        print("Favorites:")
        for movie in movies["movies"]:
            print(f"\t {movie['title']} (ID: {movie['id']})")
    else:
        print("Failed to fetch favorites:", response.status_code, response.text)

# Main function to run all tests
def run_tests():
    # 1. List all first (1 < n < 20) popular movies
    popularMovies(5)

    # 2. List movies with the same genre
    sameGenreMovies(5, 5)

    # 3. List movies with a similar runtime
    similarRuntimeMovies(5, 5)

    # 4. Generate plot bar for the given movies
    plotBarMovies([5, 6, 7])

    # 5. Be able to (un)favorite a movie + return the list of favorites
    favoriteMovie(5)
    getFavorites()



if __name__ == "__main__":
    run_tests()