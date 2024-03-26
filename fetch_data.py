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
    request = requests.get(request, timeout=30)
    target_path = tarpath
    try:
        # check the status code
        # extract tar file to project folder
        with open(target_path, "wb") as file:
            file.write(request.content)

        with tarfile.open(target_path, "r:gz") as tar_file:
            tar_file.extractall(filter="fully_trusted")

    except FileNotFoundError:
        print("File name does not exist; please try again")
