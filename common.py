import streamlit as st
import pandas as pd
from pathlib import Path

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

 # Rename columns if needed    
    df = df.rename(columns={"Holiday_Flag": "IsHoliday"})

    # Convert Date and extract features
    df["Date"] = pd.to_datetime(df["Date"])
    df["Year"] = df["Date"].dt.year
    df["Week"] = df["Date"].dt.isocalendar().week.astype(int)

    # Clean Type
    if "Type" in df.columns:
        df["Type"] = df["Type"].astype(str).str.strip().str.upper()
    return df

def render_filters(df: pd.DataFrame):
    st.sidebar.header("Filters")

        # Year filter
    years = st.sidebar.multiselect(
        "Year",
        options=sorted(df["Year"].dropna().unique()),
        default=sorted(df["Year"].dropna().unique())
    )
        # Week filter
    weeks = st.sidebar.multiselect(
        "Week",
        options=sorted(df["Week"].dropna().unique()),
        default=sorted(df["Week"].dropna().unique())
    )
        # Store filter
    stores = st.sidebar.multiselect(
        "Store",
        options=sorted(df["Store"].dropna().unique()),
        default=sorted(df["Store"].dropna().unique()) 
    )
        # Type filter
    types = st.sidebar.multiselect(
        "Type",
        options=sorted(df["Type"].dropna().unique()),
        default=sorted(df["Type"].dropna().unique())
    )

    # Apply filters
    mask = (
        df["Year"].isin(years) &
        df["Week"].isin(weeks) &
        df["Store"].isin(stores) &
        df["Type"].isin(types)
    )
    dff = df.loc[mask].copy()
    return dff
