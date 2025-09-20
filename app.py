import streamlit as st
import pandas as pd
from common import load_data, render_filters

# Page configuration
st.set_page_config(page_title="Walmart Sales Dashboard", layout="wide")

# Load dataset
DATA_PATH = "data/wallmart_final_dataset.csv"
df = load_data(DATA_PATH)
dff = render_filters(df)

# Page title
st.title("Key Performance Indicators")

# Calculate key metrics
total_sales = float(dff["Weekly_Sales"].sum())
total_stores = int(dff["Store"].nunique())
avg_weekly = dff.groupby(["Year","Week"])["Weekly_Sales"].sum().mean() if not dff.empty else 0
holiday_share = dff.loc[dff["IsHoliday"]==1, "Weekly_Sales"].sum() / total_sales * 100 if total_sales>0 else 0

# Display KPIs
st.markdown("""
<style>
:root{
  --bg: var(--secondary-background-color);
  --text: var(--text-color);
}
.kpi-grid{
  display:grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap:16px;
  margin: 8px 0 20px 0;
}
@media (max-width: 1100px){ .kpi-grid{ grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 640px){ .kpi-grid{ grid-template-columns: 1fr; } }

.kpi-card{
  background: var(--bg);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius:16px;
  padding:16px 18px;
}
.kpi-title{
  color: rgba(229,231,235,0.8);
  font-size:12px;
  letter-spacing:.08em;
  text-transform:uppercase;
}
.kpi-value{
  font-size:28px;
  font-weight:700;
  margin-top:6px;
  color: var(--text);
}
.kpi-sub{
  color: rgba(229,231,235,0.65);
  font-size:12px;
  margin-top:6px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card">
    <div class="kpi-title">Total Sales</div>
    <div class="kpi-value">${total_sales:,.0f}</div>
    <div class="kpi-sub">Sum of Weekly Sales</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-title">Total Stores</div>
    <div class="kpi-value">{total_stores}</div>
    <div class="kpi-sub">Unique store count</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-title">Avg Weekly Sales</div>
    <div class="kpi-value">${avg_weekly:,.0f}</div>
    <div class="kpi-sub">Average of weekly totals</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-title">Holiday Sales %</div>
    <div class="kpi-value">{holiday_share:,.1f}%</div>
    <div class="kpi-sub">Share during holiday weeks</div>
  </div>
</div>
""", unsafe_allow_html=True)


# Footer not
st.caption("Use the sidebar (Pages) to navigate between charts.")
