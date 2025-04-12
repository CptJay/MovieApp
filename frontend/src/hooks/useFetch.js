// src/hooks/useFetch.js
import { useState, useEffect } from 'react';
import { fetchData } from '../api/api';

export const useFetch = (endpoint) => {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const getData = async () => {
      try {
        const response = await fetchData(endpoint);
        setData(response);
      } catch (err) {
        setError('Failed to fetch data');
      }
    };

    getData();
  }, [endpoint]);  // Re-run if endpoint changes

  return { data, error };
};
