import React, { useState} from 'react';
import './Register.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEye, faEyeSlash } from '@fortawesome/free-solid-svg-icons';
import {useNavigate} from "react-router-dom";

function Register() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [passwordVisible, setPasswordVisible] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate=useNavigate();

  const togglePasswordVisibility = () => {
    setPasswordVisible(!passwordVisible);
  };
  const isValidEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const handleRegister = async (event) => {
    event.preventDefault();
    setError(""); // Clear previous errors
    setLoading(true);
  
    if (!username || !email || !password || !confirmPassword) {
      setError("All fields are required");
      setLoading(false);
      return;
    }
    if (!isValidEmail(email)) {
      setError("Invalid email format");
      setLoading(false);
      return;
    }
    if (password !== confirmPassword) {
      setError("Passwords do not match");
      setLoading(false);
      return;
    }
  
    try {
      const response = await fetch("http://127.0.0.1:5000/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username,
          email,
          password, // Plain text for now (we'll hash it later)
        }),
      });
  
      const data = await response.json();
  
      if (response.ok) {
        console.log("Registration successful:", data);
        navigate("/predict"); // Redirect on success
      } else {
        setError(data.error || "Registration failed");
      }
    } catch (error) {
      setError("Error connecting to the server");
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <>
    {loading && (
      <div className="loading-overlay">
        <div className="spinner"></div>
      </div>
    )}
        <div className="background">
          <div id="RegisterPage">
            <form id="RegisterForm" onSubmit={handleRegister}>
              <h1>Register</h1>
              <div className="input-box">
                <label>Username:</label>
                <input
                  id="user"
                  type="text"
                  placeholder="Username"
                  required
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                />
              </div>
              <div className="input-box">
              <label>Email:</label>
              <input
                type="email"
                placeholder="Email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
              <div className="input-box">
              <label>Password:</label>
              <div className="password-container">
              <input
              type={passwordVisible ? "text" : "password"} // Show password when visible
              id="password"
              placeholder="Password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              />
              <span id="togglePassword" className="eye" onClick={togglePasswordVisibility}>
              {/* Show faEyeSlash when the password is visible and faEye when hidden */}
              <FontAwesomeIcon icon={passwordVisible ? faEye : faEyeSlash} />
              </span>
             </div>
            </div>
            <div className="input-box">
              <label>Confirm Password:</label>
              <input
                type="password"
                placeholder="Confirm Password"
                required
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
              />
            </div>
            <div className="submit-button">
              <button type="submit" className="button">Register</button>
            </div>
              {error && <p style={{ color: 'red' }}>{error}</p>}
              <div className="register">
                {/* <p>Don't have an account? <a href='/register'>Register</a></p> */}
                <p>Already have an account?  <button id='loginid' onClick={() => navigate('/')}>Login</button></p>
              </div>
            </form>
          </div>
        </div>
    </>
  );
}

export default Register;
