import os

from constants import DOWNLOAD_PATH

import pandas as pd

data_folders = os.listdir(DOWNLOAD_PATH)

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
]

for folder in sorted(data_folders):
    print(f"Creating mapping for data in folder {folder}.")

    key_code_path = os.path.join(DOWNLOAD_PATH, folder, "LFS_PUMF_EPA_FGMD_variables.csv")
    key_codes = pd.read_csv(key_code_path, encoding='latin-1')

    key_codes = key_codes[[ *COLUMNS_TO_RENAME.keys() ]]
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

    key_codes = key_codes[key_codes.variable.isin(VARIABLES_OF_INTEREST)]

    for variable in VARIABLES_OF_INTEREST:
        print(f"Creating mapping for variable {variable}.")
        variable_codes = key_codes[key_codes.variable == variable].copy()
        variable_codes.drop(columns=["variable"], inplace=True)

        output_path = os.path.join(DOWNLOAD_PATH, folder, f"{variable}_codes.csv")
        variable_codes.to_csv(output_path, index=False)
        print(f"Mapping for variable {variable} saved to {output_path}.")

    print(f"Finished creating mapping for data in folder {folder}.\n")