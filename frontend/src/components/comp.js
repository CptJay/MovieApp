import React from 'react';
import { useFetch } from '../hooks/useFetch';

const YourComponent = () => {
  const { data, error } = useFetch('/movies');

  if (error) return <div>{error}</div>;

  return (
    <div>
      {data ? (
        <ul>
          {data.map((movie) => (
            <li key={movie.id}>{movie.title}</li>
          ))}
        </ul>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default YourComponent;
