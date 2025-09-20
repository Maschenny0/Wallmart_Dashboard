import streamlit as st
import plotly.express as px
from common import load_data, render_filters

#Page Title
st.title("Sales vs Fuel Price")

# Load and filter data
df = load_data("data/wallmart_final_dataset.csv")
dff = render_filters(df)

# Aggregate weekly sales and fuel price
fuel_agg = dff.groupby(["Year","Week"], as_index=False).agg(
    Weekly_Sales=("Weekly_Sales","sum"),
    Fuel_Price=("Fuel_Price","mean")
).sort_values(["Year","Week"])

# Try using OLS trendline if statsmodels is installed
try:
    import statsmodels.api as sm  
    fig = px.scatter(fuel_agg, x="Fuel_Price", y="Weekly_Sales", trendline="ols", opacity=0.7)

    # If statsmodels is not available, show scatter only
except Exception:
    st.info("statsmodels is not installed. Showing scatter plot without trendline.")
    fig = px.scatter(fuel_agg, x="Fuel_Price", y="Weekly_Sales", opacity=0.7)

#Show 
st.plotly_chart(fig, use_container_width=True)