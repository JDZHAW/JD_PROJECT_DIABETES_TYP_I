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

    daily_averages = (
        df.groupby(df[Fields.DATE.value].dt.date)
        .agg({Fields.SUGAR.value: "mean", Fields.INSULIN.value: "mean"})
        .reset_index()
    )

    daily_averages.columns = ["Datum", "Avg Blutzuckerwert", "Avg Insulindosis"]

    st.subheader("Blutzucker/Insulin pro Tag (Durchschnitt)")

    daily_averages.set_index("Datum", inplace=True)
    st.line_chart(daily_averages)

    out_of_norm = df[(df[Fields.SUGAR.value] < 3.9) | (df[Fields.SUGAR.value] > 5.6)]

    last_20_out_of_norm = out_of_norm.tail(20)
    st.subheader("Letzte 20 Ausreisser")

    scatter_data = last_20_out_of_norm[[Fields.DATE.value, Fields.SUGAR.value]]
    scatter_data.set_index(Fields.DATE.value, inplace=True)
    st.scatter_chart(scatter_data)


if __name__ == "__main__":
    main()
