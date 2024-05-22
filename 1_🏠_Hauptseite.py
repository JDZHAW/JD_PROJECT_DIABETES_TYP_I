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

    last_entries_count = 10
    create_last_sugar_and_insulin_graph(last_entries_count, df)
    create_out_of_norm_chart(last_entries_count, df)


def create_out_of_norm_chart(entries_count, df):
    df_graph = df.copy()
    st.subheader(f"Letzte {entries_count} Ausreisser")
    out_of_norm = df_graph[
        (df_graph[Fields.SUGAR.value] < 3.9) | (df_graph[Fields.SUGAR.value] > 5.6)
    ]

    last_x_out_of_norm = out_of_norm.tail(10)

    scatter_data = last_x_out_of_norm[[Fields.DATE.value, Fields.SUGAR.value]]
    scatter_data.set_index(Fields.DATE.value, inplace=True)
    st.scatter_chart(scatter_data)


def create_last_sugar_and_insulin_graph(entries_count, df):
    df_graph = df.copy()
    df_graph[Fields.DATE.value] = pd.to_datetime(df_graph[Fields.DATE.value])

    st.subheader(f"Blutzucker/Insulin Diagramm (letzte {entries_count} Einträge)")
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
        if row[Fields.TIME_OF_DAY.value] in time_map:
            return time_map[row[Fields.TIME_OF_DAY.value]]
        else:
            return row[Fields.TIME_OF_DAY.value]  # Use the time string directly

    df_graph["Time"] = df_graph.apply(determine_time, axis=1)
    df_graph["DateTime"] = pd.to_datetime(
        df_graph[Fields.DATE.value].dt.strftime("%Y-%m-%d") + " " + df_graph["Time"]
    )

    df_graph = df_graph.sort_values(by="DateTime").tail(entries_count)
    if "Kohlenhydrate" in df.columns:
        df_graph = df_graph.drop(columns=["Kohlenhydrate"])

    # Melt the DataFrame for Altair
    df_graph = df_graph.melt(id_vars="DateTime", var_name="Messwert", value_name="Wert")

    # Create the Altair chart
    chart = (
        alt.Chart(df_graph)
        .mark_bar()
        .encode(
            x=alt.X("Messwert:N", title=None, axis=alt.Axis(labels=False, ticks=False)),
            y=alt.Y("Wert:Q", title="Wert"),
            color="Messwert:N",
            column=alt.Column(
                "DateTime:T", title=None, timeUnit="monthdatehoursminutes"
            ),
        )
        .properties(width=50)
    )
    st.altair_chart(chart)


if __name__ == "__main__":
    main()
