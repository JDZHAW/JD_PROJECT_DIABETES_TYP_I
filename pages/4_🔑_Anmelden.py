##############################################################################################################
# Title: Multi-User Login and Registration Example
# Author: Samuel Wehrli, Dominik Kunz
# Date: 05.05.2024
# Institution: ZHAW - Institute for Computational Health
#
# Description:
# A Streamlit app that allows multiple users to login and register.
# The app uses a CSV file to store user credentials and pushes it to a seperate Github repository.
# The bcrypt library hashes the passwords and the binascii library to convert the hashed password to
# a hexadecimal string. The app uses the GithubContents class from the github_contents.py file to
# interact with the Github data repository. The st.secrets object stores the Github owner, repository,
# and token which are used to authenticate the Github data repository.
#
# To run the app, install the required libraries using: pip install bcrypt binascii
##############################################################################################################


import binascii

import bcrypt
import streamlit as st

from functions import utils


def login_page():
    """Login an existing user."""
    st.title("Login")
    with st.form(key="login_form"):
        st.session_state["username"] = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            authenticate(st.session_state.username, password)


def authenticate(username, password):
    """
    Initialize the authentication status.

    Parameters:
    username (str): The username to authenticate.
    password (str): The password to authenticate.
    """
    login_df = st.session_state.df_users
    login_df["username"] = login_df["username"].astype(str)

    if username in login_df["username"].values:
        stored_hashed_password = login_df.loc[
            login_df["username"] == username, "password"
        ].values[0]
        stored_hashed_password_bytes = binascii.unhexlify(
            stored_hashed_password
        )  # convert hex to bytes

        # Check the input password
        if bcrypt.checkpw(password.encode("utf8"), stored_hashed_password_bytes):
            st.session_state["authentication"] = True
            st.session_state["username"] = username
            st.session_state["name"] = login_df.loc[
                login_df["username"] == username, "name"
            ].values[0]
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Incorrect password")
    else:
        st.error("Username not found")


def main():
    st.set_page_config(page_title="Login", page_icon="🔑")
    utils.init_github()  # Initialize the GithubContents object
    utils.init_credentials()  # Loads the credentials from the Github data repository

    if not utils.is_logged_in():
        login_page()

    else:
        st.success(
            f"Hurray {st.session_state['username']}!! You are logged in.", icon="🤩"
        )
        st.switch_page("1_🏠_Hauptseite.py")


if __name__ == "__main__":
    main()
