import streamlit as st
from auth.auth import get_current_user


def initialize_session():
    """
    Initialize session variables.
    """

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "user" not in st.session_state:
        st.session_state.user = None


def check_authentication():
    """
    Check if a user is already authenticated.
    """

    user = get_current_user()

    if user:
        st.session_state.logged_in = True
        st.session_state.user = user
    else:
        st.session_state.logged_in = False
        st.session_state.user = None


def is_logged_in():
    """
    Returns True if the user is logged in.
    """

    return st.session_state.get("logged_in", False)


def get_user():
    """
    Returns the current logged-in user.
    """

    return st.session_state.get("user", None)


def clear_session():
    """
    Clears Streamlit session after logout.
    """

    st.session_state.logged_in = False
    st.session_state.user = None