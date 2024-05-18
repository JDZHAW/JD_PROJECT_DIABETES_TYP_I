import streamlit as st

from functions import utils


def main():
    if not utils.is_logged_in():
        utils.redirect_to_login()
    st.set_page_config(page_title="Alle Angaben", page_icon="📊", layout="wide")

    st.title("Alle Angaben")
    utils.add_sidebar_title()

    utils.init_dataframe()
    st.dataframe(st.session_state.df, hide_index=True, width=1000, height=500)

    utils.add_download_button()
    utils.add_logout_button()


if __name__ == "__main__":
    main()
