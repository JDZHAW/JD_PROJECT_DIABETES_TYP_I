from enum import Enum

GIT_DIABETES_CSV_FOLDER = "diabetes_data"

LOGIN_FILE = "diabetes_login_table.csv"
LOGIN_DATA_COLUMNS = ["username", "name", "password"]


class Fields(Enum):
    DATE = "Datum"
    TIME_OF_DAY = "Tageszeit"
    SUGAR = "Blutzuckerwert"
    INSULIN = "Insulindosis"
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
