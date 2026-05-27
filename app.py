import streamlit as st

from login import show_login
from dashboard import show_dashboard
from processing_page import show_processing

st.set_page_config(layout="wide")

# =========================
# INIT STATE
# =========================
if "page" not in st.session_state:
    st.session_state.page = "login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "image" not in st.session_state:
    st.session_state.image = None


# =========================
# ROUTING SYSTEM
# =========================
page = st.session_state.page

if page == "login":
    show_login()

elif page == "dashboard":
    show_dashboard()

elif page == "processing":
    show_processing()