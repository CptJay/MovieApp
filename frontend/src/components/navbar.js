import React from 'react';
import { Link } from 'react-router-dom'; // Using React Router for navigation
import logo from '../static/logo.svg'; // Import your logo image

const Navbar = () => {
  return (
    <nav className="bg-purple-900 p-4 shadow-md">
      <div className="container mx-auto flex justify-between items-center">
        <div className="text-white font-bold text-2xl">
          <Link to="/">MovieApp</Link>
        </div>
        <div className="flex items-center">
          <img className={"w-15 h-10"} src={logo} alt="Logo" />
        </div>
        <ul className="flex space-x-6">
          <li>
            <Link to="/movie" className="text-white hover:text-gray-300">
              Movie
            </Link>
          </li>
          <li>
            <Link to="/popular" className="text-white hover:text-gray-300">
              Popular
            </Link>
          </li>
          <li>
            <Link to="/favourites" className="text-white hover:text-gray-300">
              Favourites
            </Link>
          </li>
          <li>
            <Link to="/similarity" className="text-white hover:text-gray-300">
              Similarity
            </Link>
          </li>
          <li>
            <Link to="/barplot" className="text-white hover:text-gray-300">
              Bar Plot
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;