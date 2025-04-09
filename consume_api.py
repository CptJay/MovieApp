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

# Main function to run all tests
def run_tests():
    # 1. List all first 20 popular movies
    popularMovies()

if __name__ == "__main__":
    run_tests()