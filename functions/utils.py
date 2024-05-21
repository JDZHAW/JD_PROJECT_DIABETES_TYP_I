import pandas as pd
import streamlit as st

from functions.github_contents import GithubContents
from other import constants
from other.constants import Fields


def init_github():
    """Initialize the GithubContents object."""
    if "github" not in st.session_state:
        st.session_state.github = GithubContents(
            st.secrets["github"]["owner"],
            st.secrets["github"]["repo"],
            st.secrets["github"]["token"],
        )


def is_logged_in():
    """Check if the user is logged in."""
    if "authentication" not in st.session_state:
        st.session_state["authentication"] = False
    return st.session_state["authentication"]


def redirect_to_login():
    """Redirect to the login page."""
    st.switch_page("pages/4_🔑_Anmelden.py")


def init_credentials():
    """Initialize or load the dataframe."""
    if "df_users" in st.session_state:
        pass

    if st.session_state.github.file_exists(constants.LOGIN_FILE):
        st.session_state.df_users = st.session_state.github.read_df(
            constants.LOGIN_FILE
        )
    else:
        st.session_state.df_users = pd.DataFrame(columns=constants.LOGIN_DATA_COLUMNS)


def get_data_file_name():
    """Get the data file."""
    if not is_logged_in():
        return
    username = st.session_state["username"]
    return f"{constants.GIT_DIABETES_CSV_FOLDER}/{username}.csv"


def get_data_file():
    """Get the data file."""
    if not is_logged_in():
        return
    filename = get_data_file_name()
    if st.session_state.github.file_exists(filename):
        return st.session_state.github.read_df(filename)


def init_dataframe():
    """Initialize or load the dataframe."""
    data_file = get_data_file_name()
    if "df" in st.session_state and st.session_state.df is not None:
        pass
    elif st.session_state.github.file_exists(data_file):
        st.session_state.df = st.session_state.github.read_df(data_file)
    else:
        columns = [field.value for field in Fields]
        st.session_state.df = pd.DataFrame(columns=columns)


def logout():
    st.session_state["authentication"] = False
    st.session_state["username"] = None
    st.session_state["name"] = None
    st.session_state["df"] = None
    redirect_to_login()


def add_logout_button():
    st.sidebar.button("Abmelden", on_click=logout)


def add_download_button():
    dia_file = get_data_file()
    if dia_file is not None:
        download_file = dia_file.to_csv(index=False)
        st.sidebar.download_button(
            "Export CSV",
            download_file,
            "diabetes_tagebuch.csv",
            help="Export all entries data as CSV file",
        )


def add_sidebar_title():
    fullname = st.session_state["name"]
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"]::before {{
                content: "{name}";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }}
        </style>
        """.format(name=fullname),
        unsafe_allow_html=True,
    )
