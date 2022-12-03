import os

from constants import DOWNLOAD_PATH

import pandas as pd

MERGED_DATA_PATH = f"{DOWNLOAD_PATH}/merged_data.csv"
if os.path.exists(MERGED_DATA_PATH):
    os.remove(MERGED_DATA_PATH)

data_folders = os.listdir(DOWNLOAD_PATH)

KEY_CODES_FILENAME = "LFS_PUMF_EPA_FGMD_variables.csv"

COLUMNS_TO_RENAME = {
    "Variable / \nVariable": "variable",
    "Code / \nCode": "code",
    "Label - English /\nÉtiquette - Anglais": "en_label",
    "Label - French /\nÉtiquette - Francais": "fr_label",
}

VARIABLES_OF_INTEREST = [
    "naics_21",
    "prov",
    "educ",
    "noc_40",
    "age_12",
    "noc_10",    # ADDED TO SUPPORT LATER TASKS
    "lfsstat",   # ADDED TO SUPPORT LATER TASKS
    "sex",       # ADDED TO SUPPORT LATER TASKS
    "ftptmain",  # ADDED TO SUPPORT LATER TASKS
    "cowmain",   # ADDED TO SUPPORT LATER TASKS
    "whypt",     # ADDED TO SUPPORT LATER TASKS
]

for folder in sorted(data_folders):
    print(f"Creating mapping for data in folder {folder}.")

    key_code_path = os.path.join(DOWNLOAD_PATH, folder, KEY_CODES_FILENAME)
    key_codes = pd.read_csv(key_code_path, encoding='latin-1')

    key_codes = key_codes[[*COLUMNS_TO_RENAME.keys()]]
    key_codes.rename(columns=COLUMNS_TO_RENAME, inplace=True)

    """
    The structure of the CSV is such that there are "header" rows for each
    variable, but the codes for that variable are in the following rows.
    We can forward-fill the header rows into the following rows such that the
    we can access the variable name on the row that contains the code mappings.

    After that, we can drop the unneeded header rows (ie. rows with no
    associated code).
    """
    key_codes["variable"] = key_codes["variable"].fillna(method="ffill")
    key_codes.dropna(subset=["code"], inplace=True)

    # Strip out whitespace as some variable names have unneeded whitespace.
    key_codes["variable"] = key_codes["variable"].apply(lambda v: v.strip())

    key_codes = key_codes[key_codes.variable.isin(VARIABLES_OF_INTEREST)]

    for variable in VARIABLES_OF_INTEREST:
        print(f"Creating mapping for variable {variable}.")
        variable_codes = key_codes[key_codes.variable == variable].copy()
        variable_codes.drop(columns=["variable"], inplace=True)

        variable_codes.replace({"code": {"blank": None}}, inplace=True)
        variable_codes.code = variable_codes.code.astype("Int64").astype(str)

        file_path = f"{variable}_codes.csv"
        output_path = os.path.join(DOWNLOAD_PATH, folder, file_path)
        variable_codes.to_csv(output_path, index=False)
        print(f"Mapping for variable {variable} saved to {output_path}.")

    print(f"Finished creating mapping for data in folder {folder}.\n")
