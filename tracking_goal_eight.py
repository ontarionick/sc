import pandas as pd
import matplotlib.pyplot as plt


data = pd.read_csv("./data/merged_data.csv")

# Task requests that only data from January to Septempber is used.
data = data[data["SURVMNTH"] < 10]

# Question 1 - Unemployment Rate
# Unemployment rate is defined as the number of unemployed people divided
# by the number of people in the labour force.
in_labour_force = data[data["LFSSTAT"] != "Not in labour force"].copy()
in_labour_force["unemployed"] = in_labour_force["LFSSTAT"] == "Unemployed"

unemployed_count = in_labour_force.groupby("QUARTER").sum()["unemployed"]
in_labour_force_count = in_labour_force\
    .groupby("QUARTER")\
    .count()["unemployed"]
unemployment_rate = 100.0 * unemployed_count / in_labour_force_count
unemployment_rate = unemployment_rate.round(2)
print(f"Unemployment rate by quarter: {unemployment_rate}")
unemployment_rate.plot(x="QUARTER",
                       y="unemployed",
                       kind="line",
                       ylim=(0, 10),
                       xticks=range(1, 4),
                       title="Unemployment Rate by Quarter (2022)")

plt.show()

# Question 2 - Youth Tertiary Education Attainment by Province

# Note that I find it a bit odd that 15 to 19 years of age is included in
# this metric, as there is very little chance they can attain full tertiary
# education.

YOUTH_BRACKETS = ["15 to 19 years", "20 to 24 years", "25 to 29 years"]
youth = data[data["AGE_12"].isin(YOUTH_BRACKETS)].copy()


# Note that I am excluding "Some postsecondary" as I'm not sure that counts
# as attainment of tertiary education.
TERTIARY_EDUCATION = [
    "Bachelor's degree",
    "Above bachelor's degree",
    "Postsecondary certificate or diploma",
]

youth[["tertiary_education"]] = youth[["EDUC"]].isin(TERTIARY_EDUCATION)

with_tertiary_education = youth.groupby(["PROV"]).sum()["tertiary_education"]
youth_count = youth.groupby(["PROV"]).count()["tertiary_education"]
tertiary_education_rate = 100.0 * with_tertiary_education / youth_count
tertiary_education_rate = tertiary_education_rate.round(2)

tertiary_education_rate = tertiary_education_rate.sort_values(ascending=False)

print(f"Percentage of youth with tertiary education by province: \
      {tertiary_education_rate}")

tertiary_education_rate.plot(x="PROV",
                             y="tertiary_education",
                             kind="bar",
                             ylim=(0, 100),
                             title="Percentage of Youth with Tertiary Education by Province (2022)")
plt.show()

# Question 3 - Top 5 Industries for Involuntary Part-Time Employment

"""
I will be using the NAICS_21 column to determine industry.

I will also only those who are employed part-time.
"""

part_time = data[data["FTPTMAIN"] == "Part-time"].copy()
part_time["INVOLUNTARY_PT"] = ~part_time["VOLUNTARY_PT"]
involuntary_pt_count = part_time.groupby("NAICS_21").sum()["INVOLUNTARY_PT"]
total_pt_count = part_time.groupby("NAICS_21").count()["INVOLUNTARY_PT"]
involuntary_pt_rate = 100.0 * involuntary_pt_count / total_pt_count
involuntary_pt_rate = involuntary_pt_rate.round(2)
involuntary_pt_rate = involuntary_pt_rate.sort_values(ascending=False)
top_involuntary_pt_rate = involuntary_pt_rate.head(5)
print(f"Percentage of part-time workers involuntarily part-time by industry: \
    {top_involuntary_pt_rate}")

top_involuntary_pt_rate = top_involuntary_pt_rate.sort_values(ascending=True)
top_involuntary_pt_rate.plot(x="NAICS_21",
                             y="INVOLUNTARY_PT",
                             kind="barh",
                             title="Top 5 Industries for Involuntary Part-Time Employment (2022)")
plt.show()
