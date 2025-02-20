import React, { useState } from 'react';
import axios from 'axios';
import './PredictionForm.css';

function PredictionForm() {
  const [formData, setFormData] = useState({
    Name: '',
    Age: '',
    Gender: '',
    BMI: '',
    Children: '',
    Smoker: '',
    Region: '',
    Expenses: '',
    CibilScore: '' 
  });

  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setPrediction(null); // Clear previous results

    // Convert data into the correct format
    const formattedData = {
        age: Number(formData.Age),
        sex: formData.Gender.toLowerCase(),
        bmi: Number(formData.BMI),
        children: Number(formData.Children),
        smoker: formData.Smoker.toLowerCase(), 
        region: formData.Region.toLowerCase(), 
        expenses: Number(formData.Expenses),
        cibil_score: Number(formData.CibilScore) 
    };

    console.log("Submitting data:", formattedData); 

    try {
        const response = await axios.post('http://127.0.0.1:5000/predict', formattedData, {
            headers: { 'Content-Type': 'application/json' }
        });

        console.log("Response received:", response.data); 

        if (response.data && response.data.prominent_prediction !== undefined) {
            setPrediction(response.data.prominent_prediction);
        } else {
            setError("Unexpected response from server.");
        }
    } catch (error) {
        console.error("Error predicting:", error.response ? error.response.data : error.message);
        setError("An error occurred while predicting. Please try again.");
    }
  };

  return (
    <div className="PredictionForm">
      <h1>Health Insurance</h1>
      <div className="form-container"> 
        <h2>Insurance Prediction</h2>
        <form onSubmit={handleSubmit}>
          <label>Name:</label>
          <input type="text" name="Name" value={formData.Name} onChange={handleChange} required /><br />
  
          <label>Age:</label>
          <input type="number" name="Age" value={formData.Age} onChange={handleChange} required /><br />
  
          <label>Gender:</label>
          <select name="Gender" value={formData.Gender} onChange={handleChange} required>
            <option value="">Select</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
          </select><br />
  
          <label>BMI:</label>
          <input type="number" name="BMI" value={formData.BMI} onChange={handleChange} required /><br />
  
          <label>Children:</label>
          <input type="number" name="Children" value={formData.Children} onChange={handleChange} required /><br />
  
          <label>Smoker:</label>
          <select name="Smoker" value={formData.Smoker} onChange={handleChange} required>
            <option value="">Select</option>
            <option value="Yes">Yes</option>
            <option value="No">No</option>
          </select><br />
  
          <label>Region:</label>
          <select name="Region" value={formData.Region} onChange={handleChange} required>
            <option value="">Select</option>
            <option value="Northeast">Northeast</option>
            <option value="Southeast">Southeast</option>
            <option value="Northwest">Northwest</option>
            <option value="Southwest">Southwest</option>
          </select><br />
  
          <label>Expenses:</label>
          <input type="number" name="Expenses" value={formData.Expenses} onChange={handleChange} required /><br />

          <label>CIBIL Score:</label>  
          <input type="number" name="CibilScore" value={formData.CibilScore} onChange={handleChange} required /><br />
  
          <button type="submit">Submit</button>
        </form>
  
        {error && <p className="error">{error}</p>}
        {prediction !== null && (
          <p className="prediction">
            {prediction === 1 ? "✅ Eligible for insurance" : "❌ Not eligible"}
          </p>
        )}
      </div>
    </div>
  );  
}

export default PredictionForm;
