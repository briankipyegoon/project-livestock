import React from "react";
import { useNavigate } from "react-router";
import "../styles/LandingPage.css";

const LandingPage = () => {
  const navigate = useNavigate();

  const handleLoginClick = () => navigate("/login");
  const handleSignUpClick = () => navigate("/signup");

  return (
    <div className="landing-container">
      {/* Navbar */}
      <nav className="nav-bar">
        <div className="logo">Livestock</div>
        <div className="auth-buttons">
          <button className="login-btn" onClick={handleLoginClick}>
            Log In
          </button>
          <button className="signup-btn" onClick={handleSignUpClick}>
            Sign Up
          </button>
        </div>
      </nav>

      {/* Main Content */}
      <main className="main-content">
        <div className="content-wrapper">
          <h1 className="main-heading">
            We are a platform that allows you to advertise your products to the
            best selling suppliers in the field. Welcome to enjoy our services as
            fresh as your products.
          </h1>
          <button className="explore-btn" onClick={handleLoginClick}>
            Explore More
          </button>
        </div>
      </main>
    </div>
  );
};

export default LandingPage;