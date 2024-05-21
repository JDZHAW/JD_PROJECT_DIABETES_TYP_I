import streamlit as st

from functions import utils


def main():
    if not utils.is_logged_in():
        utils.redirect_to_login()

    st.set_page_config(page_title="Alle Angaben", page_icon="📊", layout="wide")

    st.title("Alle Angaben")
    utils.add_sidebar_title()
    utils.init_dataframe()

    delete_btn = st.button("Letzten Eintrag löschen")
    if delete_btn:
        if not st.session_state.df.empty:
            st.session_state.df = st.session_state.df[:-1]
            st.session_state.github.write_df(
                utils.get_data_file_name(),
                st.session_state.df,
                f"Delete last entry for {st.session_state['username']}",
            )
            st.success("Letzter Eintrag gelöscht!")
        else:
            st.error("Keine Einträge vorhanden!")

    # reverse the dataframe to show the latest entries first
    reversed_df = st.session_state.df.iloc[::-1]
    st.dataframe(reversed_df, hide_index=True, width=1000, height=500)

    utils.add_download_button()
    utils.add_logout_button()


if __name__ == "__main__":
    main()
