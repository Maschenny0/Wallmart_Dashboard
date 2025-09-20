import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from common import load_data, render_filters

#Page Title
st.title("Store Type Performance")

#Load Data
df = load_data("data/wallmart_final_dataset.csv")
dff = render_filters(df)

# Make sure Type column is present and clean
if "Type" not in dff.columns:
    # try common alternatives; add more if needed
    for alt in ["type", "store_type", "Store_Type"]:
        if alt in dff.columns:
            dff = dff.rename(columns={alt: "Type"})
            break
if "Type" not in dff.columns:
    st.error("Column 'Type' not found in dataset. Please check column names.")
    st.stop()

dff["Type"] = dff["Type"].astype(str).str.strip().str.upper()

# Base frame with all categories to guarantee A/B/C appear
base = pd.DataFrame({"Type": ["A", "B", "C"]})

# Average and Total sales by Type, left-join to base then fill missing with 0
type_avg = (
    dff.groupby("Type", as_index=False)["Weekly_Sales"].mean()
      .rename(columns={"Weekly_Sales": "Avg_Sales"})
)
type_avg = base.merge(type_avg, on="Type", how="left").fillna(0)

type_sum = (
    dff.groupby("Type", as_index=False)["Weekly_Sales"].sum()
      .rename(columns={"Weekly_Sales": "Total_Sales"})
)
type_sum = base.merge(type_sum, on="Type", how="left").fillna(0)

# Merge both and compute share %
type_merged = type_avg.merge(type_sum, on="Type", how="left")
total_sel = float(dff["Weekly_Sales"].sum())
type_merged["Share_%"] = np.where(total_sel > 0, type_merged["Total_Sales"]/total_sel*100, 0)

# Plot
type_merged = type_merged.sort_values("Avg_Sales", ascending=False)
fig = px.bar(
    type_merged, x="Type", y="Avg_Sales",
    text=type_merged["Share_%"].round(1).astype(str) + "%"
)
fig.update_traces(textposition="outside")
st.plotly_chart(fig, use_container_width=True)
