import streamlit as st
import pandas as pd
import pickle

# Load model
model = pickle.load(open("logistics_model.pkl", "rb"))

st.title("🚚 Logistics Delay Prediction App")

st.write("Enter delivery details to predict delay")

# Inputs
distance = st.number_input("Distance (km)", 0.0)
weight = st.number_input("Weight (kg)", 0.0)
traffic = st.number_input("Traffic Volume", 0.0)
hour = st.slider("Delivery Hour", 0, 23)
system_load = st.number_input("System Load", 0.0)

vehicle = st.selectbox("Vehicle Type", ["Bike", "Truck", "Van"])
weather = st.selectbox("Weather", ["Clear", "Cloudy", "Rain", "Storm"])

# Convert weather
weather_map = {"Clear":0,"Cloudy":1,"Rain":2,"Storm":3}
weather_score = weather_map[weather]

# Create base dataframe
input_data = pd.DataFrame({
    "distance_km":[distance],
    "weight_kg":[weight],
    "traffic_volume":[traffic],
    "delivery_hour":[hour],
    "system_load":[system_load],
    "weather_score":[weather_score]
})

# Add vehicle columns safely
input_data["vehicle_type_Truck"] = 0
input_data["vehicle_type_Van"] = 0

if vehicle == "Truck":
    input_data["vehicle_type_Truck"] = 1
elif vehicle == "Van":
    input_data["vehicle_type_Van"] = 1

# Prediction
if st.button("Predict Delay"):
    try:
        prediction = model.predict(input_data)

        if prediction[0] == 1:
            st.error("⚠️ High Chance of Delay")
        else:
            st.success("✅ On-Time Delivery Expected")

    except Exception as e:
        st.error(f"Error: {e}")
