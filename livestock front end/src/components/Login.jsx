import React, { useState, useContext } from 'react';
import axios from 'axios';
import { AuthContext } from '../context/AuthContext';
import '../styles/Login.css';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { handleLogin } = useContext(AuthContext);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // Make the API call to the Flask backend
      const response = await axios.post('http://localhost:5000/register', {
        email,
        password,
      });

      if (response.status === 200) {
        // If login is successful, you can pass the response data to handleLogin
        handleLogin(email, password);
        alert('Login successful!');
      }
    } catch (error) {
      console.error('Login failed:', error.response?.data?.message || error);
      alert('Invalid email or password!');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />
      <button type="submit">Login</button>
    </form>
  );
};

export default Login;