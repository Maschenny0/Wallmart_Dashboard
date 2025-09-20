import streamlit as st
import plotly.express as px
from common import load_data, render_filters

# Page title
st.title("Holiday Impact")

# Load data and apply filters
df = load_data("data/wallmart_final_dataset.csv")
dff = render_filters(df)

# Show boxplot only if we have both holiday and non-holiday weeks
if dff["IsHoliday"].nunique() > 1:
    fig = px.box(
        dff, x="IsHoliday", 
        y="Weekly_Sales", 
        labels={"IsHoliday":"Holiday (0=No, 1=Yes)"}
        )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Current filtered data does not contain both Holiday and Non-Holiday weeks to compare.")
