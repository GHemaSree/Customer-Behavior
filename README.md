# Customer Behavior Prediction System

## 🚀 Overview
This project is a **web-based system** that predicts customer behavior for insurance companies using **deep learning**. It consists of a **Flask backend** for model inference and user registration, and a **React frontend** for user interaction.

## 📌 Features
- **User Registration** with data stored in **MongoDB**  
- **Customer data input** via a web form  
- **Deep learning model** for behavior prediction  
- **Flask API** to handle predictions and user registration  
- **React frontend** for UI  
- **Data processing** using Pandas & Scikit-Learn  
- **Joblib** for model serialization  

## 🏗️ Project Structure
Customer-Behavior/ │── backend/ # Flask API & ML Model │ ├── app.py # Flask main server │ ├── train.py # Model training script │ ├── model.pkl # Trained model (ignored in Git) │ ├── database.py # MongoDB connection setup │ ├── requirements.txt # Backend dependencies │ ├── .gitignore # Ignore unnecessary files │── frontend/ # React Application │ ├── src/ # React source files │ ├── package.json # Frontend dependencies │── README.md # Project documentation │── .gitignore # Global ignore file

## 🔧 Installation & Setup

### **Backend Setup (Flask)**
1. Navigate to the `backend/` folder.  
2. Create and activate a virtual environment.  
3. Install dependencies using `requirements.txt`.  
4. Set up MongoDB connection in `database.py`.  
5. Run the Flask server (`app.py`).  

### **Frontend Setup (React)**
1. Navigate to the `frontend/` folder.  
2. Install dependencies using `npm install`.  
3. Start the React development server.  

## 🔥 API Endpoints
| Endpoint        | Method | Description                      |
|----------------|--------|----------------------------------|
| `/register`    | POST   | Register a new user (MongoDB)   |
| `/predict`     | POST   | Predict customer behavior       |

## 🛠️ Technologies Used
### **Backend**
- Flask  
- TensorFlow  
- Scikit-Learn  
- Pandas  
- Joblib  
- MongoDB  

### **Frontend**
- React  
- Axios  
- React Router  

## 👨‍💻 Contributors
- **[Hema Sree]** – Developer  
