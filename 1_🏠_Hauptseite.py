import altair as alt
import pandas as pd
import streamlit as st

from functions import utils
from other.constants import Fields


def main():
    if not utils.is_logged_in():
        utils.redirect_to_login()

    st.set_page_config(page_title="Hauptseite", page_icon="🏠", layout="wide")
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

    last_x_entries_count = 10

    st.subheader(f"Blutzucker/Insulin Diagramm (letzte {last_x_entries_count} Einträge)")
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

    # Create a new column combining Date and TimeOfDay for grouping
    df["Date_TimeOfDay"] = df["Datum"].dt.strftime("%Y-%m-%d") + " " + df["Tageszeit"]

    last_x_entries = df.tail(last_x_entries_count).copy()

    # Restructure the data for Altair
    melted_data = last_x_entries.melt(
        id_vars=["Date_TimeOfDay"],
        value_vars=["Blutzuckerwert", "Insulindosis", "Kohlenhydrate"],
        var_name="Measurement",
        value_name="Value",
    )

    # Plot using Altair
    bar_chart = (
        alt.Chart(melted_data)
        .mark_bar()
        .encode(
            x=alt.X(
                "Date_TimeOfDay:N",
                title="Datum und Tageszeit",
                axis=alt.Axis(labelAngle=45),
            ),
            y=alt.Y("Value:Q", title="Messwert"),
            color="Measurement:N",
            tooltip=["Date_TimeOfDay", "Measurement", "Value"],
        )
        .properties(
            title="Blutzuckerwert and Insulindosis Diagramm", width=800, height=400
        )
        .configure_axis(labelAngle=45)
    )

    st.altair_chart(bar_chart, use_container_width=True)

    st.subheader(f"Letzte {last_x_entries_count} Ausreisser")
    out_of_norm = df[(df[Fields.SUGAR.value] < 3.9) | (df[Fields.SUGAR.value] > 5.6)]

    last_x_out_of_norm = out_of_norm.tail(10)

    scatter_data = last_x_out_of_norm[[Fields.DATE.value, Fields.SUGAR.value]]
    scatter_data.set_index(Fields.DATE.value, inplace=True)
    st.scatter_chart(scatter_data)


if __name__ == "__main__":
    main()
