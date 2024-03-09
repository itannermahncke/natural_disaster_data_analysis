"""
This file contains code for fetching online data and porting it to a local
variable in the folder.
"""

import tarfile
import requests


def write_to_csv(request, tarpath):
    """
    This function....

    Args

    Returns
    """
    r = requests.get(request, timeout=30)
    target_path = tarpath
    try:
        # check the status code
        # extract tar file to project folder
        with open(target_path, "wb") as f:
            f.write(r.content)

        with tarfile.open(target_path, "r:gz") as f2:
            f2.extractall()

    except FileNotFoundError:
        print("File name does not exist; please try again")
