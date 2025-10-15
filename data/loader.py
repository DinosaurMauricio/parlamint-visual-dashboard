import pandas as pd
import streamlit as st


@st.cache_data
def load_data(filepath):
    df = pd.read_parquet(filepath)
    return df


@st.cache_data
def get_view_options(df):
    """Return available views based on party orientation."""
    return ["General"] + sorted(df["Party_orientation"].dropna().unique())
