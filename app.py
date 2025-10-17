import streamlit as st

from views.general import create_view
from views.general import create_sidebar, create_view
from views.party_orientation import create_orientation_view
from utils.filters import get_active_filters
from state import load_app_state

# Config
st.set_page_config(
    page_title="ParlaMint",
)

# Data
load_app_state()
df = st.session_state.df
text_df = st.session_state.text_df

# Views
st.title("ParlaMint Dashboard")
create_sidebar(df)

filters = get_active_filters(df)

if st.session_state.view_selector == "General":
    create_view(df, text_df, filters)
else:
    create_orientation_view(df, filters, st.session_state.view_selector)
