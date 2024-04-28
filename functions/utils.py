import streamlit as st

from functions.github_contents import GithubContents


def init_github():
    """Initialize the GithubContents object."""
    if "github" not in st.session_state:
        st.session_state.github = GithubContents(
            st.secrets["github"]["owner"],
            st.secrets["github"]["repo"],
            st.secrets["github"]["token"],
        )
