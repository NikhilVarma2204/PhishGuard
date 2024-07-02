# -*- coding: utf-8 -*-
"""deep_neural_network.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1L0QlSKOoRiMhvpy6GO087b_CuLweoJZZ
"""
"""
Team:

Naga Sai Nikhil Varma Mantena (101735291)
Chandana Tangellapally(101746055)
"""
import pandas as pd

# Load dataset
df = pd.read_csv('lightweight_extracted_features_dataset.csv')  # Adjust the path to your CSV file

# Filter dataset to include only numeric columns
numeric_df = pd.DataFrame()
for column in df.columns:
    temp_col = pd.to_numeric(df[column], errors='coerce')
    if not temp_col.isnull().any():  # Column can be fully converted to numeric
        numeric_df[column] = temp_col

# Assuming 'target_column_name' is the name of the target column
feature_columns = [col for col in numeric_df.columns if col != 'dot_count']
X = numeric_df[feature_columns].values
y = numeric_df['url_length'].values

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import torch
from torch.utils.data import DataLoader, TensorDataset

# Splitting dataset into training and testing set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Feature scaling
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Convert arrays to PyTorch tensors
X_train_tensor = torch.FloatTensor(X_train)
X_test_tensor = torch.FloatTensor(X_test)
y_train_tensor = torch.LongTensor(y_train)
y_test_tensor = torch.LongTensor(y_test)

# Create DataLoader for training and testing
train_loader = DataLoader(dataset=TensorDataset(X_train_tensor, y_train_tensor), batch_size=64, shuffle=True)
test_loader = DataLoader(dataset=TensorDataset(X_test_tensor, y_test_tensor), batch_size=64, shuffle=False)

import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

class DNN(nn.Module):
    def __init__(self, input_size):
        super(DNN, self).__init__()
        self.fc1 = nn.Linear(input_size, 50)  # Adjust the number of neurons as needed
        self.fc2 = nn.Linear(50, 50)          # Adjust the number of neurons as needed
        self.fc3 = nn.Linear(50, 1)           # Assuming binary classification or a single output

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# Initialize the DNN
input_size = X_train.shape[1]
model = DNN(input_size)

# Loss and optimizer
criterion = nn.MSELoss()  # Use CrossEntropyLoss for classification if necessary
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
num_epochs = 20
for epoch in range(num_epochs):
    for inputs, labels in train_loader:
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs.squeeze(), labels.float())  # Adjust for your specific task
        loss.backward()
        optimizer.step()
    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

model.eval()  # Set the model to evaluation mode
with torch.no_grad():
    correct = 0
    total = 0
    for inputs, labels in test_loader:
        outputs = model(inputs)
        predicted = outputs.round()  # Use .argmax() for classification
        total += labels.size(0)
        correct += (predicted.squeeze().int() == labels).sum().item()

print(f'Accuracy: {100 * correct / total}%')