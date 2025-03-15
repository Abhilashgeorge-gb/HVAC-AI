import joblib
import os
import pandas as pd
import random
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# MODEL FILE CONFIGURATION

MODEL_FILE = "models/hvac_model.pkl"  # Path to save the trained model
SCALER_FILE = "models/scaler.pkl"  # Path to save data scaler

# LOAD DATASET & PREPROCESS

def load_and_prepare_data():
    """ Loads the HVAC dataset and preprocesses it for training. """
    try:
        df = pd.read_csv("data/hvac_data.csv")

        # Rename columns to match expected format
        df.rename(columns={
            "outside_temp": "temperature",
            "amb_humid_1": "humidity",
            "co2_1": "co2_level",
            "summer_setpoint_temp": "desired_temperature"  # Change if using winter mode
        }, inplace=True)

        # Create an "occupancy" column if missing
        if "occupancy" not in df.columns:
            df["occupancy"] = 0  # Default value (Modify if needed)

        # Ensure necessary columns exist
        required_columns = ["temperature", "humidity", "co2_level", "occupancy", "desired_temperature"]
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Dataset missing required column: {col}")

        # Drop any rows with missing values
        df.dropna(inplace=True)

        # Split features and target
        X = df[["temperature", "humidity", "co2_level", "occupancy"]]
        y = df["desired_temperature"]

        # Scale the data
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Save the scaler for future use
        joblib.dump(scaler, SCALER_FILE)

        return X_scaled, y

    except FileNotFoundError:
        print("❌ Error: Dataset file not found!")
        return None, None
    except ValueError as e:
        print(f"❌ Error: {e}")
        return None, None

    
# ✅ TRAIN AI MODEL

def train_hvac_model():
    """ Trains a machine learning model to predict the desired temperature. """
    X, y = load_and_prepare_data()
    if X is None:
        return None  # Exit if no data is available

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Save the trained model
    joblib.dump(model, MODEL_FILE)
    print("✅ HVAC AI Model trained and saved!")


# LOAD EXISTING MODEL OR TRAIN NEW ONE

def load_model():
    """ Loads the trained model, or trains a new one if it doesn't exist. """
    if os.path.exists(MODEL_FILE):
        return joblib.load(MODEL_FILE)
    else:
        print("⚠️ No model found! Training a new one...")
        train_hvac_model()
        return joblib.load(MODEL_FILE)

# PREDICT OPTIMAL TEMPERATURE

def predict_temperature(sensor_data):
    """ Predicts the optimal temperature based on real-time sensor data. """
    model = load_model()
    scaler = joblib.load(SCALER_FILE)

    # Extract features
    input_features = [[
        sensor_data["temperature"],
        sensor_data["humidity"],
        sensor_data["co2_level"],
        sensor_data["occupancy"]
    ]]

    # Scale input data
    input_scaled = scaler.transform(input_features)

    # Predict optimal temperature
    predicted_temp = model.predict(input_scaled)[0]
    return round(predicted_temp, 2)


# ✅ CONTINUOUS LEARNING (UPDATE MODEL)

def update_model(new_data):
    """ Updates the model with new sensor data for adaptive learning. """
    df = pd.DataFrame([new_data])

    # Append new data to the dataset
    dataset_path = "data/hvac_data.csv"
    df.to_csv(dataset_path, mode='a', header=False, index=False)

    # Retrain the model
    train_hvac_model()
    print("✅ Adaptive model updated with new data!")
