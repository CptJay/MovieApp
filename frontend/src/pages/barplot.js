import React, {useState} from "react";
import {fetchData} from "../api/api";  // Import the functions

function Barplot() {
    const [movieIds, setMovieIds] = useState([]);
    const [barplotUrl, setBarplotUrl] = useState('');
    const [warning, setWarning] = useState('');
    const [message, setMessage] = useState('');
    const [loading, setLoading] = useState(false);

    const handleGetBarplot = async () => {
        try {
            const data = await fetchData(`http://127.0.0.1:5000/api/movies/bar_plot`, {movie_ids: movieIds});
            console.log(data);
            setBarplotUrl(data.plot_url.plot_url);
            if (data.plot_url.warning) {
                setWarning(data.plot_url.warning);
            }
            setLoading(false);
            setMessage('');
        } catch (error) {
            setMessage('Error fetching barplot' + error);
        }
    }

    const handleClick = () => {
        setLoading(true);
        handleGetBarplot();
    }

    return (
        <div>
            <input
                type="text"
                value={movieIds}
                onChange={(e) => setMovieIds(e.target.value.split(',').map(id => id.trim()))}
                placeholder="Enter Movie IDs (comma separated)"
                className="px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent shadow-sm"
            />
            <button
                className="mx-5 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                onClick={handleClick}>Get Barplot
            </button>
            {loading ? (
                <p>Loading...</p>
            ) : (
                barplotUrl && <img src={barplotUrl} alt="Barplot" />
            )}
            {message && <p>{message}</p>}
            {warning && <p className="text-red-500">{warning}</p>}
        </div>
    );
}

export default Barplot;