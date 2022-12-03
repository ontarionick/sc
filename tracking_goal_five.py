import pandas as pd
import matplotlib.pyplot as plt


data = pd.read_csv("./data/merged_data.csv")

# Task requests that only data from January to Septempber is used.
data = data[data["SURVMNTH"] < 10]

MANAGEMENT_NOC_CODES = [
    "Middle management occupations in trades, transportation, production and utilities",
    "Middle management occupations in retail and wholesale trade and customer services",
    "Senior management occupations",
    "Specialized middle management occupations",
]

data["is_management"] = data["NOC_40"].isin(MANAGEMENT_NOC_CODES)

in_management = data.groupby("SEX").sum()["is_management"]
total_count = data.groupby("SEX").count()["is_management"]

in_management_rate = round(100.0 * in_management / total_count, 2)

print(f"Percentage in management occupations by sex: {in_management_rate}")
in_management_rate.plot(kind="bar", title="Percentage in Management Occupation by Sex")
plt.show()
