import React from 'react';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import Navbar from './components/navbar';  // Import the Navbar component
import Home from './pages/home';  // Import the Home component
import MoviePage from './pages/movie';  // Import the Movie component
import Favourites from './pages/favourites';  // Import the Favourites component
import Popular from "./pages/popular";
import SimilarMovies from "./pages/similar";
import Barplot from "./pages/barplot";


function App() {
    return (
        <Router>
            <Navbar/>
            <div className="container mx-auto p-4">
                <Routes>
                    <Route path="/" element={<Home/>}/>
                    <Route path="/movie" element={<MoviePage/>}/>
                    <Route path="/favourites" element={<Favourites/>}/>
                    <Route path="/popular" element={<Popular/>}/>
                    <Route path="/similar" element={<SimilarMovies/>}/>
                    <Route path="/barplot" element={<Barplot/>}/>
                </Routes>
            </div>
        </Router>
    );
}

export default App;