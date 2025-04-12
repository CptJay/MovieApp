import React, { useState } from "react";
import { fetchData} from "../api/api";

function Popular() {
    const [popularMovies, setPopularMovies] = useState([]);
    const [amount , setAmount] = useState(8);
    const [message, setMessage] = useState("");
    const [loading, setLoading] = useState(false);

    const hanledleGetPopularMovies = async () => {
        try {
            const data = await fetchData(`http://127.0.0.1:5000/api/movies/popular`, {amount});
            console.log(data);
            setPopularMovies(data.movies);
            setLoading(false);
            setMessage("");
        } catch (error) {
            setMessage("Error fetching popular movies" + error);
        }
    }
    const handleClick = () => {
        hanledleGetPopularMovies();
    };

    return (
        <div>
            <input
                type="text"
                value={amount}
                onChange={(e) => setAmount(parseInt(e.target.value) || 0)}
                placeholder="Enter Amount"
                className="px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent shadow-sm"
            />
            <button
                className="mx-5 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                onClick={handleClick}>Get Popular Movies
            </button>
            {loading ? (
                <p>Loading...</p>
            ) : (
                popularMovies && popularMovies.length > 0 ? (
                    <ul>
                        {popularMovies.map((movie) => (
                            <li key={movie.id} className="mb-2">
                                <p className="font-bold">{movie.title} (ID: {movie.id})</p>
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p> {popularMovies.length === 0 ? "No popular movies found." : ""} </p>
                )
            )}
            {message && <p>{message}</p>}
        </div>
    );
}

export default Popular;