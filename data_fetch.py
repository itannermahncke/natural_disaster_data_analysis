# This file contains code for fetching online data and porting it to a local
# variable in the folder.

import tarfile
import requests


def write_to_csv():
    """
    This function....

    Args

    Returns
    """
    r = requests.get(
        "https://www.ncei.noaa.gov/archive/archive-management-system/OAS/bin/prd/jquery/download/209268.17.17.tar.gz",
        timeout=30,
    )
    target_path = "/209268.17.17.tar.gz"
    try:
        # check the status code
        # extract tar file to project folder
        with open(target_path, "wb") as f:
            f.write(r.content)

        with tarfile.open(target_path, "r:gz") as f2:
            f2.extractall()

    except FileNotFoundError:
        print("File name does not exist; please try again")
