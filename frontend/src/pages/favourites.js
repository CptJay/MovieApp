/*
    Gives the user a list of all the liked movies.
 */

import React, {useState, useEffect} from 'react';
import {postData} from '../api/api';  // Import the functions

function Favourites() {
    const [likedMovies, setLikedMovies] = useState([]);
    const [message, setMessage] = useState('');
    const [loading, setLoading] = useState(true);

    const handleGetLikedMovies = async () => {
        try {
            const response = await fetch('http://127.0.0.1:5000/api/movies/favourites')
            const data = await response.json();
            console.log(data);
            setLikedMovies(data.movies);
            setLoading(false);
            setMessage('');
        } catch (error) {
            setMessage('Error fetching liked movies' + error);
        }
    }

    useEffect(() => {
        handleGetLikedMovies();
    }, []);

    return (
        <div>
            <h2 className="text-2xl font-bold mb-4">Liked Movies</h2>
            {loading ? (
                <p>Loading...</p>
            ) : (
                likedMovies && likedMovies.length > 0 ? (
                    <ul>
                        {likedMovies.map((movie) => (
                            <li key={movie.id} className="mb-2">
                                <p className="font-bold">{movie.title} (ID: {movie.id})</p>
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p>No liked movies found.</p>
                )
            )}
            {message && <p>{message}</p>}
        </div>
    );
}

export default Favourites;