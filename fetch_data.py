"""
This file contains code for fetching online data and porting it to a local
variable in the folder.

This file uses two imports to help retrieve the data: tarfile and
requests.
requests is used to query the National Centers for Environmental Information
(NCEI) for the dataset that we want to use and put it in a folder (line 24).
tarfile is used to extract the data (line 33) from its natural format
(a tar file that upon extraction yields a csv we can analyze with pandas).
"""

import tarfile
import requests


def write_to_csv(request, tarpath):
    """
    Given a website link to a file containing a dataset and the name of a
    destination folder (which must have the same name as the folder being
    downloaded and extracted), create the destination folder with the extracted
    dataset in it.

    Args:
        request: a string representing the link to the download for the NCEI
        dataset. This is "hardcoded" because none of our work is possible
        without downloading and using the dataset.
        tarpath: a string representing the destination folder for the
        downloaded and extracted dataset.
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
