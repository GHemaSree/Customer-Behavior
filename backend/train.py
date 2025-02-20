import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib

# Define the RNN model
class RNNModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(RNNModel, self).__init__()
        self.rnn = nn.RNN(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        out, _ = self.rnn(x.unsqueeze(1))  # Add sequence dimension
        out = self.fc(out[:, -1, :])  # Use last timestep
        return self.softmax(out)  # Apply Softmax activation

# Ensure this part runs only when train.py is executed directly
if __name__ == '__main__':
    # Load dataset
    file_path = "insurance_modified.csv"
    df = pd.read_csv(file_path)

    # Encode categorical variables
    label_encoders = {}
    for col in ['sex', 'smoker', 'region']:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le

    # Select features and target
    features = ['age', 'sex', 'bmi', 'children', 'smoker', 'region', 'expenses', 'cibil_score']
    X = df[features].values
    y = df['prominent'].values

    # Normalize features
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    # Convert to tensors
    X_tensor = torch.tensor(X, dtype=torch.float32)
    y_tensor = torch.tensor(y, dtype=torch.long)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X_tensor, y_tensor, test_size=0.2, random_state=42)

    # Model parameters
    INPUT_SIZE = len(features)
    HIDDEN_SIZE = 16
    OUTPUT_SIZE = 2

    # Initialize model
    model = RNNModel(INPUT_SIZE, HIDDEN_SIZE, OUTPUT_SIZE)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # Training loop
    epochs = 100
    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        
        # Forward pass
        outputs = model(X_train)
        
        # Calculate loss
        loss = criterion(outputs, y_train)
        
        # Backpropagation
        loss.backward()
        optimizer.step()
        
        # Print loss every 10 epochs
        if (epoch + 1) % 10 == 0:
            print(f"Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}")

    # Calculate final accuracy after training
    model.eval()
    with torch.no_grad():
        outputs = model(X_train)  # Get model predictions
        predictions = torch.argmax(outputs, dim=1)
        correct = (predictions == y_train).sum().item()
        accuracy = correct / y_train.size(0) * 100  # Convert to percentage

    print(f"\nFinal Accuracy: {accuracy:.2f}%")

    # Save the model and scaler
    torch.save(model.state_dict(), "model.pth")
    joblib.dump(scaler, "scaler.pkl")
    print("Model and scaler saved successfully!")
