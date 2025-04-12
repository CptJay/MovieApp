import React, {useEffect, useState} from 'react';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import Navbar from './components/navbar';  // Import the Navbar component
import Home from './pages/home';  // Import the Home component


function App() {
    return (
        <Router>
            <Navbar/>
            <div className="container mx-auto p-4">
                <Routes>
                    <Route path="/" element={<Home/>}/>
                    <Route path="/movie" element={<div>Movie Page</div>}/>
                </Routes>
            </div>
        </Router>
    );
}

export default App;

// function App() {
//     const [movie, setMovie] = useState(null);
//
//     useEffect(() => {
//         fetch('http://127.0.0.1:5000/api/movies/2')
//             .then(response => response.json())
//             .then(data => {
//                 setMovie(data.movie);
//             })
//             .catch(error => {
//                 console.log('Error fetching data:', error);
//             });
//     }, []);
//
//     if (!movie) {
//         return <div>Loading...</div>;
//     }
//
//     return (
//         <div>
//             <h1>{movie.title}</h1>
//             <img src={`https://image.tmdb.org/t/p/w500${movie.poster_path}`} alt={movie.title}/>
//             <p>{movie.overview}</p>
//             <p>Release Date: {movie.release_date}</p>
//             <p>Genres: {movie.genres.map(genre => genre.name).join(', ')}</p>
//         </div>
//     );
// }
//
// export default App;
