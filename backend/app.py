from flask import Flask, request, jsonify
import torch
import numpy as np
import joblib
import os
from flask_cors import CORS
from train import RNNModel
from pymongo import MongoClient
from datetime import datetime

# Paths
MODEL_PATH = "model.pth"
SCALER_PATH = "scaler.pkl"

INPUT_SIZE = 8
HIDDEN_SIZE = 16
OUTPUT_SIZE = 2

# Check if model files exist
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file '{MODEL_PATH}' not found!")

if not os.path.exists(SCALER_PATH):
    raise FileNotFoundError(f"Scaler file '{SCALER_PATH}' not found!")

# Load model
print("Loading model...")
model = RNNModel(INPUT_SIZE, HIDDEN_SIZE, OUTPUT_SIZE)
model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))
model.eval()
print("Model loaded successfully.")

# Load scaler
print("Loading scaler...")
scaler = joblib.load(SCALER_PATH)
print("Scaler loaded successfully.")

# MongoDB Connection
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "insurance"
COLLECTION_NAME = "details"

try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    raise

# Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

@app.route('/')
def home():
    return "Flask API for Prominent Customer Prediction is Running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        print("Received data:", data)

        required_features = ['age', 'sex', 'bmi', 'children', 'smoker', 'region', 'expenses', 'cibil_score']
        
        # Check for missing fields
        missing_keys = [key for key in required_features if key not in data]
        if missing_keys:
            return jsonify({'error': f'Missing fields: {missing_keys}'}), 400
        
        # Mapping categorical values to numbers
        sex_mapping = {'male': 0, 'female': 1}
        smoker_mapping = {'no': 0, 'yes': 1}
        region_mapping = {'northeast': 0, 'southeast': 1, 'northwest': 2, 'southwest': 3}

        # Validate categorical inputs
        if data['sex'].lower() not in sex_mapping:
            return jsonify({'error': "Invalid value for 'sex'. Expected: 'male' or 'female'"}), 400
        if data['smoker'].lower() not in smoker_mapping:
            return jsonify({'error': "Invalid value for 'smoker'. Expected: 'yes' or 'no'"}), 400
        if data['region'].lower() not in region_mapping:
            return jsonify({'error': "Invalid value for 'region'. Expected: 'northeast', 'southeast', 'northwest', 'southwest'"}), 400
        
        # Convert input data
        try:
            input_data = np.array([[
                float(data['age']),
                sex_mapping[data['sex'].lower()],
                float(data['bmi']),
                float(data['children']),
                smoker_mapping[data['smoker'].lower()],
                region_mapping[data['region'].lower()],
                float(data['expenses']),
                float(data['cibil_score'])
            ]])
        except ValueError as ve:
            return jsonify({'error': f'Invalid numeric input: {str(ve)}'}), 400

        # Apply scaler transformation
        input_data = scaler.transform(input_data)

        input_tensor = torch.tensor(input_data, dtype=torch.float32)

        # Make prediction
        with torch.no_grad():
            output = model(input_tensor)
            predicted_class = torch.argmax(output, dim=1).item()

        print(f"Predicted class: {predicted_class}")

        # Save prediction to MongoDB
        prediction_record = {
            "age": data['age'],
            "sex": data['sex'],
            "bmi": data['bmi'],
            "children": data['children'],
            "smoker": data['smoker'],
            "region": data['region'],
            "expenses": data['expenses'],
            "cibil_score": data['cibil_score'],
            "prediction": predicted_class,
            "timestamp": datetime.utcnow()
        }
        collection.insert_one(prediction_record)
        print("Prediction saved to MongoDB.")

        return jsonify({'prominent_prediction': predicted_class})

    except Exception as e:
        print("Error in /predict:", str(e))
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

        
USER_COLLECTION = db["users"]  # Separate collection for users

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json

        # Store user details in "users" collection instead of "details"
        user_record = {
            "username": data['username'],
            "email": data['email'],
            "password": data['password'],  
            "registered_at": datetime.utcnow()
        }
        USER_COLLECTION.insert_one(user_record)  # Save to "users" collection

        return jsonify({'message': 'Registration successful!'}), 201

    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500



if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True)
