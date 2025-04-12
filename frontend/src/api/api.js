// src/api/api.js

// Fetch data from the backend API (GET method)
export const fetchData = async (endpoint) => {
  try {
    const response = await fetch(endpoint);
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return await response.json();  // Parse the JSON response
  } catch (error) {
    console.error('Error fetching data:', error);
    throw error;  // Re-throw error for the component to handle
  }
};

// POST data to the backend (Optional, if you need it)
export const postData = async (endpoint, data) => {
  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',  // Set content type to JSON
      },
      body: JSON.stringify(data),  // Stringify the payload
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    return await response.json();  // Return parsed response
  } catch (error) {
    console.error('Error posting data:', error);
    throw error;
  }
};

// PUT data to the backend (Optional, if you need it)
export const putData = async (endpoint, data) => {
  try {
    const response = await fetch(endpoint, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',  // Set content type to JSON
      },
      body: JSON.stringify(data),  // Stringify the payload
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    return await response.json();  // Return parsed response
  } catch (error) {
    console.error('Error putting data:', error);
    throw error;
  }
};
