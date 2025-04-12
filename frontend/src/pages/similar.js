import React, {useState} from "react";
import {fetchData} from "../api/api";  // Import the functions

function SimilarMovies() {
    const [movieId, setMovieId] = useState('');
    const [similarMovies, setSimilarMovies] = useState([]);
    const [message, setMessage] = useState('');
    const [loading, setLoading] = useState(false);
    const [amount, setAmount] = useState('');
    const [runtimeDifference, setRuntimeDifference] = useState('');

    const handleGetSimilarGenre = async () => {
        try {
            const data = await fetchData(`http://127.0.0.1:5000/api/movies/${movieId}/same_genre`, {amount});
            setSimilarMovies(data.movies);
            setLoading(false);
            setMessage('');
        } catch (error) {
            setMessage('Error fetching similar movies' + error);
        }
    }

    const handleGetSimilarRuntime = async () => {
        try {
            const data = await fetchData(`http://127.0.0.1:5000/api/movies/${movieId}/same_runtime`, {
                amount: amount,
                runtime_diff: runtimeDifference
            });
            setSimilarMovies(data.movies);
            setLoading(false);
            setMessage('');
        } catch (error) {
            setMessage('Error fetching similar movies' + error);
        }
    }

    const handleGenreClick = () => {
        setLoading(true);
        handleGetSimilarGenre();
    }

    const handleRuntimeClick = () => {
        setLoading(true);
        handleGetSimilarRuntime();
    }

    return (
        <div>
            <input
                type="text"
                value={movieId}
                onChange={(e) => setMovieId(e.target.value)}
                placeholder="Enter Movie ID"
                className="px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent shadow-sm"
            />
            <input
                type="text"
                value={amount}
                onChange={(e) => setAmount(parseInt(e.target.value) || 0)}
                placeholder="Enter Amount"
                className="px-4 py-2 mx-5 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent shadow-sm"
            />
            <input
                type="text"
                value={runtimeDifference}
                onChange={(e) => setRuntimeDifference(parseInt(e.target.value) || 0)}
                placeholder="Enter Runtime Difference"
                className="px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent shadow-sm"
            />
            <button
                className="mx-5 bg-purple-500 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                onClick={handleGenreClick}>Get Similar Movies by Genre
            </button>
            <button
                className="mx-5 bg-purple-500 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                onClick={handleRuntimeClick}>Get Similar Movies by Runtime
            </button>
            {loading ? (
                <p>Loading...</p>
            ) : (
                similarMovies && similarMovies.length > 0 ? (
                    <ul>
                        {similarMovies.map((movie) => (
                            <li key={movie.id} className="mb-2">
                                <p className="font-bold">{movie.title} (ID: {movie.id})</p>
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p>{similarMovies.length === 0 ? "No similar movies found." : ""}</p>
                )
            )}
            {message && <p>{message}</p>}
        </div>
    );

}

export default SimilarMovies;