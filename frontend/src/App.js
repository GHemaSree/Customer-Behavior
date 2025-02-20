import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom'; // Import Navigate
import Register from './components/Register'; // Your Register component
import PredictionForm from './components/PredictionForm'; // Your PredictionForm component

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          {/* Redirect root path to the Register component */}
          <Route path="/" element={<Navigate to="/register" />} /> 
          <Route path="/register" element={<Register />} />
          <Route path="/predict" element={<PredictionForm />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
