import os
import requests
import zipfile
import io
import shutil
from constants import DOWNLOAD_PATH, YEAR_MONTH_PAIRS

BASE_URL = "https://www150.statcan.gc.ca/n1/pub/71m0001x/2021001/{year}-{month}-CSV.zip"


def download_data(year, month):
    """
    Download LFS Microdata File for a given year and month into memory,
    then unzip it to disk.
    """

    month = str(month).zfill(2)
    url = BASE_URL.format(year=year, month=month)
    save_path = os.path.join(DOWNLOAD_PATH, f"{year}-{month}/")

    if os.path.exists(save_path):
        shutil.rmtree(save_path)

    response = requests.get(url, stream=True)
    zipped_data = zipfile.ZipFile(io.BytesIO(response.content))
    zipped_data.extractall(save_path)

for year, month in YEAR_MONTH_PAIRS:
    print(f"Downloading LFS Microdata File for {year}-{month}.")
    download_data(year, month)
    print(f"Finished downloading LFS Microdata File for {year}-{month}.\n")
