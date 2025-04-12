/* This file is resposible for being able to take input from the user.
The data is either a string, number or a list of strings.
The data is then sent to the backend using the api.js file.
 */

import React, { useState } from 'react';
import { postData, putData, deleteData } from '../api/api';  // Import the API functions
import { useNavigate } from 'react-router-dom';  // Import the useNavigate hook

const Input = ({ type, endpoint, initialData }) => {
    const [inputValue, setInputValue] = useState(initialData || '');  // State for input value
    const navigate = useNavigate();  // Initialize the navigate function

    // Function to handle input change
    const handleInputChange = (e) => {
        setInputValue(e.target.value);
    };

    // Function to handle form submission
    const handleSubmit = async (e) => {
        e.preventDefault();  // Prevent default form submission

        try {
        let response;

        if (type === 'POST') {
            response = await postData(endpoint, { data: inputValue });
        } else if (type === 'PUT') {
            response = await putData(endpoint, { data: inputValue });
        } else if (type === 'DELETE') {
            response = await deleteData(endpoint);
        }

        console.log('Response:', response);  // Log the response
        // navigate('/');  // Navigate to the home page after submission
        } catch (error) {
        console.error('Error:', error);  // Log any errors
        }
    };

    return (
        <form onSubmit={handleSubmit}>
        <input type="text" value={inputValue} onChange={handleInputChange} />
        <button type="submit">{type}</button>
        </form>
    );
}

export default Input;