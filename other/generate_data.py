import random
from datetime import datetime, timedelta

import pandas as pd
from constants import Fields, TimeOfDay

time_of_day_choices = [time.value for time in TimeOfDay]
feelings = ["gut", "mittel", "schlecht"]


def random_date(start, end):
    return start + timedelta(days=random.randint(0, int((end - start).days)))


end_date = datetime.now()
start_date = end_date - timedelta(days=30)

sugar_mean = 5.5
sugar_std_dev = 1.5


num_entries = 100
data = {field.value: [] for field in Fields}

for _ in range(num_entries):
    date = random_date(start_date, end_date).strftime("%Y-%m-%d")
    time_of_day = random.choice(time_of_day_choices)
    if time_of_day == TimeOfDay.ADDITIONAL.value:
        time_of_day = datetime.now().strftime("%H:%M")
    sugar = round(random.gauss(sugar_mean, sugar_std_dev), 1)
    insulin = random.randint(0, 50)
    carbs = random.randint(0, 100)
    feeling = random.choice(feelings)
    feeling_desc = "Random description " + str(random.randint(1, 100))

    data[Fields.DATE.value].append(date)
    data[Fields.TIME_OF_DAY.value].append(time_of_day)
    data[Fields.SUGAR.value].append(sugar)
    data[Fields.INSULIN.value].append(insulin)
    data[Fields.CARBS.value].append(carbs)
    data[Fields.FEELING.value].append(feeling)
    data[Fields.FEELING_DESC.value].append(feeling_desc)

test_df = pd.DataFrame(data)
test_df.to_csv("~/Desktop/test_data.csv", index=False)
