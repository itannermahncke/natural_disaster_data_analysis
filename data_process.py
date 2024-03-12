import pandas as pd


# function that writes the csv to a variable
def read_csv_to_var(file_name):
    """
    docs
    """
    return pd.read_csv(file_name)


# function that takes a disaster name and index and returns the region desination
def geo_locator(disaster_name, index):
    """
    docs
    """
    region_array = [
        "Western",
        "Midwest",
        "Southern",
        "Northeast",
    ]
    location_array = [
        "Northwest",
        "Southwest",
        "Plains",
        "Southeast",
    ]
    disaster_location = []
    for _ in region_array:
        if _ in disaster_name:
            disaster_location.append(_ + str(index))
    if len(disaster_location) > 1:
        return None
    for _ in location_array:
        if _ in disaster_name:
            disaster_location.append(_ + str(index))
    if len(disaster_location) > 2:
        return None
    if len(disaster_location) == 2:
        if "Plains" in disaster_location[0] or "Plains" in disaster_location[1]:
            if (
                "Midwest" in disaster_location[0]
                or "Midwest" in disaster_location[1]
            ):
                return [x for x in disaster_location if "Plains" not in x]
            return None
        if (
            "Southwest" in disaster_location[0]
            or "Southwest" in disaster_location[1]
        ):
            if "West" in disaster_location[0] or "West" in disaster_location[1]:
                return [x for x in disaster_location if "Southwest" not in x]
            return None
        if (
            "Southeast" in disaster_location[0]
            or "Southeast" in disaster_location[1]
        ):
            if (
                "South" in disaster_location[0]
                or "South" in disaster_location[1]
            ):
                return [x for x in disaster_location if "Southeast" not in x]
            return None
        if (
            "Northwest" in disaster_location[0]
            or "Northwest" in disaster_location[1]
        ):
            if "West" in disaster_location[0] or "West" in disaster_location[1]:
                return [x for x in disaster_location if "Northwest" not in x]
            return None
    return disaster_location


# function that parses the date and returns the year
