import streamlit as st
from data.loader import load_data
from utils.text_analyzer import TextAnalyzer
from config import DATA_PATH, TEXT_DATA_PATH, LANG_MODEL, SPACY_PREPROCESSED


def load_app_state():
    if "df" not in st.session_state:
        with st.spinner("Loading data..."):
            st.session_state.df = load_data(DATA_PATH)

    if "text_df" not in st.session_state:
        with st.spinner("Loading sentences..."):
            st.session_state.text_df = load_data(TEXT_DATA_PATH)

    if "pre_processed_df" not in st.session_state:
        with st.spinner("Loading preprocessed text..."):
            st.session_state.pre_processed_df = load_data(SPACY_PREPROCESSED)

    if "view_selector" not in st.session_state:
        st.session_state.view_selector = "General"

    # if "nlp" not in st.session_state:
    with st.spinner("Loading spaCy..."):
        # st.session_state.nlp = TextAnalyzer(LANG_MODEL)
        TextAnalyzer(LANG_MODEL)
