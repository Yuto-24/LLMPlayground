""" Page to compare the models """

import streamlit as st

############# Page Setting #############
PAGE_TITLE = "Compare"
PAGE_ICON = "🏹"

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="wide",
)
# Header
st.header(f"{PAGE_ICON} {PAGE_TITLE}")
