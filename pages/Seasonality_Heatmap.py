import streamlit as st
import plotly.express as px
from common import load_data, render_filters

#Page Title
st.title("Seasonality Heatmap (Store × Week)")

# Load dataset
df = load_data("data/wallmart_final_dataset.csv")
dff = render_filters(df)

# Group sales by Store and Week
heat = dff.groupby(["Store","Week"], as_index=False)["Weekly_Sales"].sum()

# Pivot data to create a matrix (Store vs Week)
pivot = heat.pivot(index="Store", columns="Week", values="Weekly_Sales").fillna(0)

# Create heatmap

fig = px.imshow(
    pivot.values,
    labels=dict(x="Week", y="Store", color="Sales"),
    x=pivot.columns, 
    y=pivot.index,
    aspect="auto"
)

#show
st.plotly_chart(fig, use_container_width=True)