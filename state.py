import streamlit as st
from data.loader import load_data
from config import DATA_PATH, TEXT_DATA_PATH


def load_app_state():
    if "df" not in st.session_state:
        with st.spinner("Loading data..."):
            st.session_state.df = load_data(DATA_PATH)

    if "text_df" not in st.session_state:
        with st.spinner("Loading utterances..."):
            st.session_state.text_df = load_data(TEXT_DATA_PATH)

    if "view_selector" not in st.session_state:
        st.session_state.view_selector = "General"

    return st.session_state.df, st.session_state.text_df
