import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import load_data, render_filters

# Page title
st.title("Economic Factors Impact (CPI & Unemployment vs Sales)")

# Load data and apply filters
df = load_data("data/wallmart_final_dataset.csv")
dff = render_filters(df)

# Group data by Date and calculate sales, CPI, unemployment
eco = dff.groupby("Date", as_index=False).agg(
    Weekly_Sales=("Weekly_Sales","sum"),
    CPI=("CPI","mean"),
    Unemployment=("Unemployment","mean"),
    IsHoliday=("IsHoliday","max")
).sort_values("Date")

# Create subplot with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Scatter(x=eco["Date"], y=eco["Weekly_Sales"], name="Weekly Sales"), secondary_y=False)
fig.add_trace(go.Scatter(x=eco["Date"], y=eco["CPI"], name="CPI"), secondary_y=True)
fig.add_trace(go.Scatter(x=eco["Date"], y=eco["Unemployment"], name="Unemployment"), secondary_y=True)

# Highlight holidays
for d in eco.loc[eco["IsHoliday"]==1, "Date"]:
    fig.add_vrect(x0=d, x1=d, fillcolor="LightSalmon", opacity=0.2, line_width=0)
# Axis labels
fig.update_yaxes(title_text="Weekly Sales", secondary_y=False)
fig.update_yaxes(title_text="CPI / Unemployment", secondary_y=True)

# Show chart
st.plotly_chart(fig, use_container_width=True)