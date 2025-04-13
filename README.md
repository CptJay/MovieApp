Welcome to my MovieApp. 

This project is a simple movie application that allows users to search for movies (ID based), view details, and manage their favorite movies. 

The app is built using a custom API that interacts with the TMDB API to fetch movie data. The backend is built with Flask, and the frontend is built with React.

## Installation
- run_api.sh (run_api.bat for Windows) to start the Flask API. This will also install the dependencies.
- run_script.sh (run_script.bat for Windows) to execute the consume_api.py script.
  - consume_api.py will tests the API endpoints.
- run_frontend.sh (run_frontend.bat for Windows) to start the React frontend.

 
## Features (Backend)
- [x] Search for movies by ID
- [x] Like and unlike movies 
- [x] Get list of favorite movies
- [x] Get popular movies
- [x] Get movies with similar genres
- [x] Get movies with similar runtime

## Features (Frontend)
- Same as the backend

## Technologies Used
- [x] React (node + npm)
- [x] Tailwind CSS
- [x] Flask
- [x] Flask-CORS
- [x] Flassger (Flask + Swagger): API documentation
- [x] [TMDB](https://developers.themoviedb.org/3) API: 236e9d003709eb55cf700526b1c268f0
- [x] [Quickchart](https://quickchart.io/) API: None
