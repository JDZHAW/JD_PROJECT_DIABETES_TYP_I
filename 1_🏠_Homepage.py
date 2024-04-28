import streamlit as st

from functions import utils

if __name__ == "__main__":
    st.set_page_config(page_title="Homepage", page_icon="🏠")
    st.title("Diabetes Tagebuch")
    utils.init_github()
