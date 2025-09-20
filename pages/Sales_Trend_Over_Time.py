import streamlit as st
import plotly.express as px
from common import load_data, render_filters

#Page Title
st.title("Sales Trend Over Time")

# Load data and apply filters
df = load_data("data/wallmart_final_dataset.csv")
dff = render_filters(df)

# Aggregate weekly sales by date
trend = dff.groupby("Date", as_index=False)["Weekly_Sales"].sum().sort_values("Date")

# Create line chart
fig = px.line(trend, x="Date", y="Weekly_Sales", title=None)

# Highlight holidays if the column exists
if "IsHoliday" in dff.columns:
    holiday_dates = dff.loc[dff["IsHoliday"] == 1, "Date"].drop_duplicates().sort_values()
    for d in holiday_dates:
        fig.add_vrect(x0=d, x1=d, fillcolor="LightSalmon", opacity=0.25, line_width=0)

#Show
st.plotly_chart(fig, use_container_width=True)
