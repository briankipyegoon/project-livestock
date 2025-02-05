import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Signup from './components/Signup';
import Login from './components/Login';
import LivestockForm from './components/LivestockForm';
import LivestockList from './components/LivestockList';
import './index.css';
import { AuthProvider } from './context/AuthContext';

const App = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route path="/" element={<LivestockList />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/login" element={<Login />} />
          <Route path="/livestock" element={<LivestockList />} />
          <Route path="/create-livestock" element={<LivestockForm />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
};

export default App;