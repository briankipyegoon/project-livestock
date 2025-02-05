import React, { useState, useEffect } from 'react';
import '../styles/LivestockList.css';

const LivestockList = () => {
  const [livestockPosts, setLivestockPosts] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLivestockPosts([
      {
        id: 1,
        breed: 'Angus Cattle',
        age: '2 years',
        weight: '1200 lbs',
        price: 1200,
        location: 'Texas',
        image: 'https://example.com/cattle-image.jpg'
      },
    ]);
  }, []);

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="livestock-list">
      <h2>Livestock Posts</h2>
      {livestockPosts.length === 0 ? (
        <p>No livestock posts available.</p>
      ) : (
        livestockPosts.map((post) => (
          <div key={post.id} className="livestock-card">
            <img src={post.image} alt={post.breed} />
            <h3>{post.breed}</h3>
            <p>Age: {post.age}</p>
            <p>Weight: {post.weight}</p>
            <p>Price: ${post.price}</p>
            <p>Location: {post.location}</p>
          </div>
        ))
      )}
    </div>
  );
};

export default LivestockList;