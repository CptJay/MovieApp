/* This file contains functions to interact with the backend API.

 */

// POST data to the backend
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

// PUT data to the backend
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

// DELETE data from the backend
export const deleteData = async (endpoint) => {
  try {
    const response = await fetch(endpoint, {
      method: 'DELETE',
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    return await response.json();  // Return parsed response
  } catch (error) {
    console.error('Error deleting data:', error);
    throw error;
  }
};
