import pandas as pd
import streamlit as st

from functions import utils
from other.constants import Fields


def main():
    if not utils.is_logged_in():
        utils.redirect_to_login()

    st.set_page_config(page_title="Homepage", page_icon="🏠", layout="wide")
    utils.add_sidebar_title()

    utils.init_github()
    utils.init_dataframe()

    if not utils.is_logged_in():
        return

    utils.add_download_button()
    utils.add_logout_button()

    df = utils.get_data_file()
    if df is None:
        st.title("Keine Daten vorhanden")
        return

    df[Fields.DATE.value] = pd.to_datetime(df[Fields.DATE.value])

    st.subheader("Blutzucker/Insulin Diagramm (letzte 20 Einträge)")
    time_map = {
        "nüchtern": "06:00",
        "vor dem Frühstück": "09:00",
        "vor dem Mittagessen": "12:00",
        "vor dem Abendessen": "16:00",
        "vor dem Schlafen": "21:00",
        "zusätzlich": "00:00",  # Default to midnight if 'zusätzlich'
    }

    # Function to determine the time
    def determine_time(row):
        if row["Tageszeit"] in time_map:
            return time_map[row["Tageszeit"]]
        else:
            return row["Tageszeit"]  # Use the time string directly

    df["Time"] = df.apply(determine_time, axis=1)
    df["DateTime"] = pd.to_datetime(
        df["Datum"].dt.strftime("%Y-%m-%d") + " " + df["Time"]
    )

    df = df.sort_values(by="DateTime")

    last_20_entries = df.tail(20)

    last_20_entries.set_index("DateTime", inplace=True)
    combined_data = last_20_entries[["Blutzuckerwert", "Insulindosis"]]
    st.line_chart(combined_data)

    st.subheader("Letzte 20 Ausreisser")
    out_of_norm = df[(df[Fields.SUGAR.value] < 3.9) | (df[Fields.SUGAR.value] > 5.6)]

    last_20_out_of_norm = out_of_norm.tail(20)

    scatter_data = last_20_out_of_norm[[Fields.DATE.value, Fields.SUGAR.value]]
    scatter_data.set_index(Fields.DATE.value, inplace=True)
    st.scatter_chart(scatter_data)


if __name__ == "__main__":
    main()
