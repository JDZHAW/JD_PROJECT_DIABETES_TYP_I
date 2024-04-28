import streamlit as st
import pandas as pd
from enum import Enum
from functions.github_contents import GithubContents

DATA_FILE = "diabetes_data.csv"


class Fields(Enum):
    DATE = "Datum"
    TIME = "Uhrzeit"
    SUGAR = "Blutzuckerwert"
    INSULIN = "Insulingabe"
    CARBS = "Kohlenhydrate"
    FEELING = "Wohlbefinden"


def init_github():
    """Initialize the GithubContents object."""
    if "github" not in st.session_state:
        st.session_state.github = GithubContents(
            st.secrets["github"]["owner"],
            st.secrets["github"]["repo"],
            st.secrets["github"]["token"],
        )


def init_dataframe():
    """Initialize or load the dataframe."""
    if "df" in st.session_state:
        pass
    elif st.session_state.github.file_exists(DATA_FILE):
        st.session_state.df = st.session_state.github.read_df(DATA_FILE)
    else:
        columns = [field.value for field in Fields]
        st.session_state.df = pd.DataFrame(columns=columns)


def create_input_form():
    date = st.sidebar.date_input(Fields.DATE.value)
    time = st.sidebar.time_input(Fields.TIME.value)
    sugar = st.sidebar.number_input(Fields.SUGAR.value, step=0.1)
    insulin = st.sidebar.number_input(Fields.INSULIN.value, step=0.1)
    carbs = st.sidebar.number_input(Fields.CARBS.value, step=1)
    feeling = st.sidebar.selectbox(Fields.FEELING.value, ["gut", "mittel", "schlecht"])

    entry = {
        Fields.DATE.value: date,
        Fields.TIME.value: time,
        Fields.SUGAR.value: sugar,
        Fields.INSULIN.value: insulin,
        Fields.CARBS.value: carbs,
        Fields.FEELING.value: feeling,
    }

    for key, value in entry.items():
        if value is None:
            st.sidebar.error(f"{key} darf nicht leer sein!")
            return

    # Check if there is a row with the same date and time
    if not st.session_state.df.empty:
        date_str = date.strftime("%Y-%m-%d")
        time_str = time.strftime("%H:%M:%S")

        mask = (st.session_state.df["Datum"] == date_str) & (
            st.session_state.df["Uhrzeit"] == time_str
        )
        if st.session_state.df[mask].shape[0] > 0:
            st.sidebar.error("Eintrag für Datum und Uhrzeit existiert bereits!")
            return

    submit_btn = st.sidebar.button("Hinzufügen")
    if submit_btn:
        entry_df = pd.DataFrame([entry])

        mask = (st.session_state.df["Datum"] == date_str) & (
            st.session_state.df["Uhrzeit"] == time_str
        )
        if st.session_state.df[mask].shape[0] > 0:
            st.sidebar.error("Eintrag für Datum und Uhrzeit existiert bereits!")
            return

        st.session_state.df = pd.concat(
            [st.session_state.df, entry_df], ignore_index=True
        )

        date_str = date.strftime("%Y%m%d")
        time_str = time.strftime("%H%M%S")
        date_timestamp = f"{date_str}-{time_str}"
        current_timestamp = pd.Timestamp.now().strftime("%Y%m%d%H%M%S")
        msg = f"Add entry for {date_timestamp} at {current_timestamp}"

        st.session_state.github.write_df(DATA_FILE, st.session_state.df, msg)


def display_dataframe():
    """Display the DataFrame in the app."""
    if not st.session_state.df.empty:
        st.dataframe(st.session_state.df)
    else:
        st.write("No data to display.")


if __name__ == "__main__":
    st.title("Diabetes Tagebuch")
    init_github()
    init_dataframe()
    create_input_form()
    display_dataframe()
