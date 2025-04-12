import React from 'react';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import Navbar from './components/navbar';  // Import the Navbar component
import Home from './pages/home';  // Import the Home component
import MoviePage from './pages/movie';  // Import the Movie component
import Favourites from './pages/favourites';  // Import the Favourites component


function App() {
    return (
        <Router>
            <Navbar/>
            <div className="container mx-auto p-4">
                <Routes>
                    <Route path="/" element={<Home/>}/>
                    <Route path="/movie" element={<MoviePage/>}/>
                    <Route path="/favourites" element={<Favourites/>}/>
                </Routes>
            </div>
        </Router>
    );
}

export default App;