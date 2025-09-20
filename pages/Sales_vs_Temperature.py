import streamlit as st
import plotly.express as px
from common import load_data, render_filters

# Page title
st.title("Sales vs Temperature")

# Load dataset
df = load_data("data/wallmart_final_dataset.csv")
dff = render_filters(df)

# Scatter plot between Temperature and Weekly Sales
fig = px.scatter(
    dff, 
    x="Temperature", 
    y="Weekly_Sales",
    color="IsHoliday" if "IsHoliday" in dff.columns else None,
    opacity=0.6
)

#Show 
st.plotly_chart(fig, use_container_width=True)