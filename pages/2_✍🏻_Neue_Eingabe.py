import pandas as pd
import streamlit as st

from functions import utils
from other.constants import Fields, TimeOfDay


def pick_time_to_use(time_of_day, additional_time):
    if time_of_day == TimeOfDay.ADDITIONAL.value:
        return additional_time
    return time_of_day


def create_input_form():
    st.sidebar.title("Neue Eingabe")
    date = st.sidebar.date_input(Fields.DATE.value)
    filtered_df = filter_dataframe(date)
    st.dataframe(filtered_df, hide_index=True)

    existing_times = filtered_df["Tageszeit"].unique()
    existing_times = [
        time for time in existing_times if time != TimeOfDay.ADDITIONAL.value
    ]
    time_of_day_options = [
        time.value for time in TimeOfDay if time.value not in existing_times
    ]

    time_of_day = st.sidebar.selectbox(Fields.TIME_OF_DAY.value, time_of_day_options)

    additional_time = None
    if time_of_day == TimeOfDay.ADDITIONAL.value:
        additional_time = st.sidebar.time_input("Uhrzeit")
    sugar = st.sidebar.number_input(
        f"{Fields.SUGAR.value} (mmol/l)",
        step=0.1,
        value=4.5,
        help="Referenzbereich: 3.9 - 5.6 mmol/l",
    )
    insulin = st.sidebar.number_input(f"{Fields.INSULIN.value} (IE)", step=1)
    carbs = st.sidebar.number_input(f"{Fields.CARBS.value} (gramm)", step=1)
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
        data_file = utils.get_data_file_name()
        st.session_state.github.write_df(data_file, st.session_state.df, msg)
        st.success("Eintrag hinzugefügt!")


def filter_dataframe(date=None):
    """Only show the data from todays date. Keep date only in datum field like '2024-05-18'"""
    if date is None:
        date = pd.Timestamp.now().strftime("%Y-%m-%d")

    df = st.session_state.df.copy()
    df[Fields.DATE.value] = pd.to_datetime(df[Fields.DATE.value]).dt.date

    date_obj = pd.to_datetime(date).date()
    return df[df[Fields.DATE.value] == date_obj]


def main():
    if not utils.is_logged_in():
        utils.redirect_to_login()

    st.set_page_config(page_title="Neue Eingabe", page_icon="✍️", layout="wide")
    st.title("Heutige Angaben")
    utils.add_sidebar_title()

    utils.init_github()
    utils.init_dataframe()
    create_input_form()


if __name__ == "__main__":
    main()
