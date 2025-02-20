#  Customer Behavior Prediction System

##  Overview
This project is a **web-based system** that predicts customer behavior for insurance companies using **deep learning**. It consists of a **Flask backend** for model inference and user registration, and a **React frontend** for user interaction.

##  Features
✅ **User Registration** with data stored in **MongoDB**  
✅ **Customer Data Input** via a web form  
✅ **Deep Learning Model** for behavior prediction  
✅ **Flask API** for predictions and user registration  
✅ **React Frontend** for UI  
✅ **Data Processing** using Pandas & Scikit-Learn  
✅ **Joblib** for model serialization  

##  Project Structure

### **Backend (Flask)**
- `backend/`
  - `app.py` → Main Flask server  
  - `train.py` → Model training script  
  - `model.pkl` → Trained model (ignored in Git)  
  - `database.py` → MongoDB connection setup  
  - `requirements.txt` → Backend dependencies  
  - `.gitignore` → Ignore unnecessary files  

### **Frontend (React)**
- `frontend/`
  - `src/` → React source files  
  - `package.json` → Frontend dependencies  

### **Root Directory**
- `README.md` → Project documentation  
- `.gitignore` → Global ignore file  

## Installation & Setup

### **Backend Setup (Flask)**
1. Navigate to the `backend/` folder.  
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows

##  Installation & Setup

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

##  API Endpoints
| Endpoint        | Method | Description                      |
|----------------|--------|----------------------------------|
| `/register`    | POST   | Register a new user (MongoDB)   |
| `/predict`     | POST   | Predict customer behavior       |

## Technologies Used
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
