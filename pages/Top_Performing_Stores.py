import streamlit as st
import plotly.express as px
from common import load_data, render_filters

# Page title
st.title("Top Performing Stores")

# Load data 
df = load_data("data/wallmart_final_dataset.csv")
dff = render_filters(df)

# Aggregate sales per store + add context (avg CPI / Unemployment)
store_agg = dff.groupby("Store", as_index=False).agg(
    Total_Sales=("Weekly_Sales","sum"),
    Avg_CPI=("CPI","mean"),
    Avg_Unemp=("Unemployment","mean")
).sort_values("Total_Sales", ascending=False).head(10)

# Horizontal bar chart 

fig = px.bar(
    store_agg.sort_values("Total_Sales"),
    x="Total_Sales", 
    y="Store",
    orientation="h",
    hover_data={"Avg_CPI":":.2f","Avg_Unemp":":.2f"},
)

#Show Chart
st.plotly_chart(fig, use_container_width=True)