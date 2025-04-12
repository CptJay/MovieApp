/* this is the movie page. There are 1 endpoint connected to this page:
- /api/movies/:id with post, put and delete methods
- the user can put an id in a box and click the button to get the movie
- the user can also delete a movie by clicking the delete button
- the user can also update(like) the movie by clicking the like button
*/

import React, {useState} from 'react';
import {postData, putData, deleteData} from '../api/api';  // Import the functions

function MoviePage() {
    const [movieId, setMovieId] = useState('');
    const [movieData, setMovieData] = useState(null);
    const [message, setMessage] = useState('');

    const handleGetMovie = async () => {
        try {
            const response = await fetch(`http://127.0.0.1:5000/api/movies/${movieId}`);
            const data = await response.json();
            setMovieData(data.movie);
            setMessage('');
        } catch (error) {
            setMessage('Error fetching movie' + error);
        }
    };

    const handleDeleteMovie = async () => {
        try {
            await deleteData(`http://127.0.0.1:5000/api/movies/${movieId}`);
            setMessage('Movie deleted successfully');
            setMovieData(null); // Clear movie data
        } catch (error) {
            setMessage('Error deleting movie' + error);
        }
    };

    const handleLikeMovie = async () => {
        const movieToUpdate = {like: true};
        try {
            await putData(`http://127.0.0.1:5000/api/movies/${movieId}`, movieToUpdate);
            setMessage('Movie liked successfully');
        } catch (error) {
            setMessage('Error liking movie' + error);
        }
    };

    return (
        <div>
            <input
                type="text"
                value={movieId}
                onChange={(e) => setMovieId(e.target.value)}
                placeholder="Enter Movie ID"
                className="px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent shadow-sm"
            />
            <button
                className="mx-5 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                onClick={handleGetMovie}>Get Movie
            </button>
            <button
                className="mx-5 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                onClick={handleDeleteMovie}>Delete Movie
            </button>
            <button
                className="mx-5 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                onClick={handleLikeMovie}>Like Movie
            </button>
            {message && <p>{message}</p>}
            {movieData && (
                <div className={"my-2"}>
                    <h1 className={"text-2xl font-bold"}>Movie Details</h1>
                    <h2 className="text-xl font-semibold my-2">Title: {movieData.title} (ID = {movieData.id})</h2>
                    <p className="text-lg">Description: {movieData.overview}</p>
                    <img
                        className="w-1/2 h-auto my-2"
                        src={`https://image.tmdb.org/t/p/w500${movieData.poster_path}`} alt={movieData.title}/>

                </div>
            )}
        </div>
    );
}

export default MoviePage;