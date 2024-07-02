# -*- coding: utf-8 -*-
"""compare_models.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GsLQGhZZ1EkqfxlmoSfzJKYguJS7bWX-
"""
"""
Team:

Naga Sai Nikhil Varma Mantena (101735291)
Chandana Tangellapally(101746055)
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

# Load dataset
dataset_path = 'lightweight_extracted_features_dataset.csv'  # Update this to your dataset path
df = pd.read_csv(dataset_path)

# Encode the 'type' column to numeric values
label_encoder = LabelEncoder()
df['type_encoded'] = label_encoder.fit_transform(df['type'])

# Define features and target variable
X = df[['has_ip', 'dot_count', 'url_length', 'has_redirection', 'has_javascript', 'uses_https']].values
y = df['type_encoded'].values

# Split the dataset into training (80%) and testing (20%) sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Define models
models = {
    "Naive Bayes": GaussianNB(),
    "Logistic Regression": LogisticRegression(max_iter=1000, solver='liblinear', tol=0.1),
    "SVM": SVC()
}

# Train and evaluate models
for name, model in models.items():
    model.fit(X_train_scaled, y_train)  # Train model
    y_pred = model.predict(X_test_scaled)  # Predict on test set
    accuracy = accuracy_score(y_test, y_pred)  # Calculate accuracy
    print(f"{name} Accuracy: {accuracy:.4f}")