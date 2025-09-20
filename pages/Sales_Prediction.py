# pages/Sales_Prediction.py

import streamlit as st
import pandas as pd
import pickle
import numpy as np

# Page configuration
st.set_page_config(page_title="Sales Prediction", layout="wide")

st.title("Weekly Sales Prediction")
st.write("This page uses our trained Linear Regression model to predict weekly sales based on your inputs.")

# --- 1. Load Model and Scaler ---
# We use st.cache_resource to load the model only once and store it in cache
@st.cache_resource
def load_model():
    """Load the saved model, scaler, and feature list."""
    try:
        with open('models/linear_regression_model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('models/scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        with open('models/selected_features.pkl', 'rb') as f:
            features = pickle.load(f)
        return model, scaler, features
    except FileNotFoundError:
        st.error("Model files not found. Please ensure 'models' directory is in the root and contains the .pkl files.")
        return None, None, None

model, scaler, selected_features = load_model()

# --- 2. User Inputs in the Sidebar ---
st.sidebar.header("Input Features")

if model is not None:
    # Create input fields for all the features the model was trained on
    size = st.sidebar.number_input("Store Size", min_value=30000, max_value=220000, value=150000, step=1000)
    cpi = st.sidebar.number_input("Consumer Price Index (CPI)", min_value=120.0, max_value=230.0, value=211.0, step=0.1)
    unemployment = st.sidebar.number_input("Unemployment Rate", min_value=3.0, max_value=15.0, value=8.1, step=0.1)
    month = st.sidebar.slider("Month of the Year", min_value=1, max_value=12, value=2, step=1)
    
    is_holiday = st.sidebar.selectbox("Is it a Holiday Week?", ("No", "Yes"))
    store_type = st.sidebar.selectbox("Store Type", ("A", "B", "C"))

    # When the user clicks the button, we proceed with prediction
    if st.sidebar.button("Predict Sales"):
        
        # --- 3. Preprocess Inputs ---
        
        # Convert categorical inputs to the format the model expects
        is_holiday_binary = 1 if is_holiday == "Yes" else 0
        type_b = 1 if store_type == "B" else 0
        type_c = 1 if store_type == "C" else 0
        
        # Create a DataFrame from the user inputs
        # The keys MUST match the feature names
        input_data = pd.DataFrame({
            'Size': [size],
            'CPI': [cpi],
            'Unemployment': [unemployment],
            'IsHoliday': [is_holiday_binary],
            'Month': [month],
            'Type_B': [type_b],
            'Type_C': [type_c]
        })

        # Separate numerical and binary columns to apply scaling correctly
        numerical_cols = ['Size', 'CPI', 'Unemployment', 'Month']
        
        # Apply the SAME scaling as we did in training
        input_data[numerical_cols] = scaler.transform(input_data[numerical_cols])
        
        # Ensure the columns are in the EXACT same order as during training
        input_data = input_data[selected_features]
        
        # --- 4. Make Prediction ---
        
        # Add the constant (intercept) term for the statsmodels model
        input_data_with_const = np.c_[np.ones(input_data.shape[0]), input_data]
        
        # Get the prediction
        prediction = model.predict(input_data_with_const)
        predicted_sales = prediction[0]

        # --- 5. Display Result ---
        st.subheader("Prediction Result")
        st.metric("Predicted Weekly Sales", f"${predicted_sales:,.2f}")
        
        st.success("The prediction is based on the provided input features.")
        st.balloons()
else:
    st.warning("Model is not loaded. Cannot proceed with prediction.")