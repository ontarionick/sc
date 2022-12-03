import os

from constants import DOWNLOAD_PATH

import pandas as pd
import pandas.api.types as ptypes

MERGED_DATA_PATH = f"{DOWNLOAD_PATH}/merged_data.csv"
if os.path.exists(MERGED_DATA_PATH):
    os.remove(MERGED_DATA_PATH)

data_folders = os.listdir(DOWNLOAD_PATH)

VARIABLES_TO_APPLY_MAPPING = [
    "LFSSTAT",
    "SEX",
    "FTPTMAIN",
    "WHYPT",
    "PROV",      # ADDED TO SUPPORT LATER TASKS
    "AGE_12",    # ADDED TO SUPPORT LATER TASKS
    "NAICS_21",  # ADDED TO SUPPORT LATER TASKS
    "NOC_10",    # ADDED TO SUPPORT LATER TASKS
    "NOC_40",    # ADDED TO SUPPORT LATER TASKS
    "EDUC",      # ADDED TO SUPPORT LATER TASKS
    "COWMAIN",   # ADDED TO SUPPORT LATER TASKS
]

VARIABLES_TO_KEEP = [
    "SURVMNTH",
    "LFSSTAT",
    "PROV",
    "AGE_12",
    "SEX",
    "EDUC",
    "NAICS_21",
    "NOC_10",
    "NOC_40",
    "COWMAIN",
    "FTPTMAIN",
    "QUARTER",
    "VOLUNTARY_PT",
]

mapped_dataframes = []


def pub_path(folder):
    year, month = folder.split("-")
    return f"pub{month}{year[-2:]}.csv"


def recode_variable(variable, mapping):
    return variable.map(mapping)


for folder in sorted(data_folders):
    print(f"Applying mappings for data in folder {folder}.")
    month_data_path = os.path.join(DOWNLOAD_PATH, folder, pub_path(folder))
    month_data = pd.read_csv(month_data_path)

    for variable in VARIABLES_TO_APPLY_MAPPING:
        print(f"Applying mapping for variable {variable}.")
        file_path = f"{variable.lower()}_codes.csv"
        mapping_path = os.path.join(DOWNLOAD_PATH, folder, file_path)

        mapping = pd.read_csv(mapping_path)
        mapping[["code"]] = mapping[["code"]].astype("Int64").astype(str)
        mapping = mapping.set_index("code").to_dict()["en_label"]

        month_data[[variable]] = month_data[[variable]]\
            .astype("Int64")\
            .astype(str)

        month_data = month_data.replace({variable: mapping})
        print(f"Applied mapping for variable {variable}.")
    print(f"Applied mappings for data in folder {folder}.\n")

    month_data["QUARTER"] = pd.to_datetime(folder).quarter
    mapped_dataframes.append(month_data)

print("Merging data into final dataset.")
merged_data = pd.concat(mapped_dataframes)

"""
There's an old Statistics Canada definition here:
https://www150.statcan.gc.ca/n1/pub/75-001-x/00200/5608-eng.html

If the respondent is usually working less than 30 hours per week, they are
considered to be working part-time. If the respondent states they do not
want to work full-time, they are considered voluntary part-time. They are
then asked to state the reason why they chose to work part-time. We can
derive the VOLUNTARY_PT variable by setting it to True when the WHYPT
is not blank, and False otherwise.

That doesn't quite seem to work here, as in later steps I'm seeing 0
values for everybody, so I'm going to try a different approach by
manually coding anything except for business reasons as voluntary.
That being said, this definition seems a bit incomplete still as it is
arguable some things such as caring for children or illness / disability
are not voluntary!
"""

VOLUNTARY_PT_CODES = [
    "Personal preference",
    "Own illness or disability",
    "Going to school",
    "Other personal or family responsibilities",
    "Other reasons",
    "Caring for children",
]

merged_data["VOLUNTARY_PT"] = merged_data["WHYPT"].isin(VOLUNTARY_PT_CODES)
merged_data = merged_data[[*VARIABLES_TO_KEEP]]

# TODO: Add data quality checks here.

merged_data.to_csv(MERGED_DATA_PATH, index=False)
print("Finished merging data into final dataset.")
