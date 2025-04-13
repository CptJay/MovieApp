**First name:** Yassir

**Last name:** Chebaa Amimou    



**Explain how your API follows the RESTful principles.**
(using notes from class)

- Made sure to describe recourses, not applications and tried to avoid using verbs in the URL e.g. 
  ```
  - /movies/5
  - /movies/popular
  - /movies/favourites
  ```

- Avoid non-RESTful URLs, in python there is a clean way to add the endpoints e.g.:
  - ``api.add_resource(Movie, '/movies/<int:movie_id>')``

- I used the correct HTTP methods for each endpoint:
  - GET: to retrieve data
  - POST: to create new data
  - PUT: to update existing data
  - DELETE: to remove data

- Keep the URIs short, simple and meaningful with a clear structure (hackable up the tree):
    - ``/movies/{movie_id}/same_genre``

- Overall the recources are human-readable and self-descriptive.
- Query parameters are also only used for the parameters.




**[Optional] Motivate your design decisions. Are there any designs you considered but decided not to implement? Why?**

- I used a prefix for the endpoints to make it clear that they are part of the API. I used `/api/` as a prefix. (defined once in the app.py file).
- Use core noun and keep correlated functionality together.
- I've only worked with RESTful APIs before, so I didn't consider other designs like SOAP.


**Discuss efficiency. How would you improve the performance optimization of your API?**

- Obviously, caching is the first thing that comes to mind, but I didn't implement it in this project.
- I used two sets (datacontainers) to store temporary data in memory *locally*. This is not the most efficient way to store data, but it is the easiest way to implement the API. I would use a database to store those data aswell.
- At the moment we only use max 20 movies for certain requests, but in reality this could be more and would need pagination to handle the data efficiently.



**Fault tolerance: Can your API handle faulty requests? If so, what kind of errors does it address, and how are they handled?**

- Yes, the API can handle faulty requests.
- For all path parameters, I check wether the type is correct and wether the value is valid.
- The same goes for the query parameters.
- If the request is invalid, I return a 400 error with a message explaining the error.
- If the API call to TMDB fails, I handle the error accordingly. e.g.
  - Let's say we want to check the bar plot for 3 movies, but it happens that one of the ID, even though it's a valid ID, is not in the TMDB database. I handle this by returning a 400 error with a message explaining that the movie is not found (500). but still remain to plot the bar for the other two movies and notify the user that the movie wasn't available (check frontend).
- A very useful way of handling errors in python is to use the `try` and `except` statements. I used this in my code to handle errors when calling the TMDB API. If an error occurs, I catch it and return a 500 error with a message explaining the error.



**[Extension] Carefully discuss your extensions. Describe what you have added and why. If you implemented additional technologies or algorithms, explain what they do, and how they function.
Note: Your extensions will be primarily evaluated based on the report, so ensure that each extension is documented with sufficient depth.**

- I've implemented a frontend using React and Tailwind CSS. The frontend is a simple movie application that allows users to search for movies by ID, view details, and manage their favorite movies. The frontend interacts with the Flask API.
- There's a homepage that welcomes the user and explains the options in the navbar.
- The navbar contains the following options:
  - Movie
    - Search for a movie by ID
    - Like and unlike a movie
    - Delete a movie (blacklisted)
  - Popular
    - View popular movies
  - Favourites
    - View favourite movies
  - Similarity
    - View movies with similar genres
    - View movies with similar runtime
  - Bar plot
    - Get a bar plot of the average score for the given  movies



**How many hours did you spend on this assignment? (used for statistics)**

- 20~25 hours (including research)