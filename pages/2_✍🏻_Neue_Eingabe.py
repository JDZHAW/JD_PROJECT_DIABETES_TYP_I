from enum import Enum

import pandas as pd
import streamlit as st

from functions import utils
from other.constants import GIT_DIABETES_CSV_FILENAME as DATA_FILE


class Fields(Enum):
    DATE = "Datum"
    TIME_OF_DAY = "Tageszeit"
    SUGAR = "Blutzuckerwert"
    INSULIN = "Insulingabe"
    CARBS = "Kohlenhydrate"
    FEELING = "Wohlbefinden"
    FEELING_DESC = "Wohlbefinden Beschreibung"


class TimeOfDay(Enum):
    SOBER = "nüchtern"
    BEFORE_BREAKFAST = "vor dem Frühstück"
    BEFORE_LUNCH = "vor dem Mittagessen"
    BEFORE_DINNER = "vor dem Abendessen"
    BEFORE_SLEEP = "vor dem Schlafen"
    ADDITIONAL = "zusätzlich"


def pick_time_to_use(time_of_day, additional_time):
    if time_of_day == TimeOfDay.ADDITIONAL.value:
        return additional_time
    return time_of_day


def create_input_form():
    date = st.sidebar.date_input(Fields.DATE.value)
    time_of_day = st.sidebar.selectbox(
        Fields.TIME_OF_DAY.value, [time.value for time in TimeOfDay]
    )
    additional_time = None
    if time_of_day == TimeOfDay.ADDITIONAL.value:
        additional_time = st.sidebar.time_input("Uhrzeit")
    sugar = st.sidebar.number_input(
        Fields.SUGAR.value,
        step=0.1,
        value=4.5,
        help="Referenzbereich: 3.9 - 5.6 mmol/l",
    )
    insulin = st.sidebar.number_input(Fields.INSULIN.value, step=1)
    carbs = st.sidebar.number_input(Fields.CARBS.value, step=1)
    feeling = st.sidebar.selectbox(Fields.FEELING.value, ["gut", "mittel", "schlecht"])
    feeling_desc = st.sidebar.text_area(Fields.FEELING_DESC.value)

    entry = {
        Fields.DATE.value: date,
        Fields.TIME_OF_DAY.value: pick_time_to_use(time_of_day, additional_time),
        Fields.SUGAR.value: sugar,
        Fields.INSULIN.value: insulin,
        Fields.CARBS.value: carbs,
        Fields.FEELING.value: feeling,
        Fields.FEELING_DESC.value: feeling_desc,
    }

    for key, value in entry.items():
        if key == Fields.FEELING_DESC.value:
            continue
        if value is None:
            st.sidebar.error(f"{key} darf nicht leer sein!")
            return

    # Check if there is a row with the same date and time of day
    if not st.session_state.df.empty:
        date_str = date.strftime("%Y-%m-%d")
        time_str = entry[Fields.TIME_OF_DAY.value]

        mask = (st.session_state.df["Datum"] == date_str) & (
            st.session_state.df["Tageszeit"] == time_str
        )
        if st.session_state.df[mask].shape[0] > 0:
            st.sidebar.error("Eintrag für Datum und Tageszeit existiert bereits!")
            return

    submit_btn = st.sidebar.button("Hinzufügen")
    if submit_btn:
        entry_df = pd.DataFrame([entry])

        st.session_state.df = pd.concat(
            [st.session_state.df, entry_df], ignore_index=True
        )

        date_str = date.strftime("%Y-%m-%d")
        time_str = entry[Fields.TIME_OF_DAY.value]

        current_timestamp = pd.Timestamp.now().strftime("%Y%m%d%H%M%S")
        msg = f"Add entry for '{date_str} - {time_str}' at {current_timestamp}"
        st.session_state.github.write_df(DATA_FILE, st.session_state.df, msg)


def init_dataframe():
    """Initialize or load the dataframe."""
    if "df" in st.session_state:
        pass
    elif st.session_state.github.file_exists(DATA_FILE):
        st.session_state.df = st.session_state.github.read_df(DATA_FILE)
    else:
        columns = [field.value for field in Fields]
        st.session_state.df = pd.DataFrame(columns=columns)


def display_dataframe():
    """Display the DataFrame in the app."""
    st.dataframe(st.session_state.df)


utils.init_github()
init_dataframe()
create_input_form()
display_dataframe()
