import binascii

import bcrypt
import pandas as pd
import streamlit as st

from functions import utils
from other.constants import LOGIN_DATA_COLUMNS, LOGIN_FILE


def register_page():
    """Register a new user."""
    st.title("Register")
    with st.form(key="register_form"):
        new_username = st.text_input("Username")
        new_name = st.text_input("Full Name")
        new_password = st.text_input("Password", type="password")
        if st.form_submit_button("Register"):
            # check if any field is empty
            if not new_username or not new_name or not new_password:
                st.error("All fields are required.")
                return

            hashed_password = bcrypt.hashpw(
                new_password.encode("utf8"), bcrypt.gensalt()
            )  # Hash the password
            hashed_password_hex = binascii.hexlify(
                hashed_password
            ).decode()  # Convert hash to hexadecimal string

            # Check if the username already exists
            if new_username in st.session_state.df_users["username"].values:
                st.error("Username already exists. Please choose a different one.")
                return
            else:
                new_user = pd.DataFrame(
                    [[new_username, new_name, hashed_password_hex]],
                    columns=LOGIN_DATA_COLUMNS,
                )
                st.session_state.df_users = pd.concat(
                    [st.session_state.df_users, new_user], ignore_index=True
                )

                # Writes the updated dataframe to GitHub data repository
                st.session_state.github.write_df(
                    LOGIN_FILE, st.session_state.df_users, "added new user"
                )
                st.success("Registration successful! You can now log in.")


def main():
    st.set_page_config(page_title="Register", page_icon="📝")
    utils.init_github()  # Initialize the GithubContents object
    utils.init_credentials()  # Loads the credentials from the Github data repository
    register_page()


if __name__ == "__main__":
    main()
