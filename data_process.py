"""
Helper functions for processing the data in our CSV into useful, bite-size
dataframes that can be used to plot information.
"""

import pandas as pd


# this function writes the csv to a variable
def read_csv_to_var(file_name):
    """
    docs
    """
    return pd.read_csv(
        file_name,
        header=0,
        names=[
            "Name",
            "Disaster",
            "Begin Date",
            "End Date",
            "Total CPI-Adjusted Cost (Millions of Dollars)",
            "Deaths",
        ],
    ).drop([0])


# function that takes a disaster name and index and returns the region desination
def geo_locator(disaster_name):
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
            disaster_location.append(_)
    if len(disaster_location) > 1:
        return ["Empty"]
    for _ in location_array:
        if _ in disaster_name:
            disaster_location.append(_)
    if len(disaster_location) > 2:
        return ["Empty"]
    if len(disaster_location) == 2:
        if "Plains" in disaster_location[0] or "Plains" in disaster_location[1]:
            if (
                "Midwest" in disaster_location[0]
                or "Midwest" in disaster_location[1]
            ):
                return [x for x in disaster_location if "Plains" not in x]
            return ["Empty"]
        if (
            "Southwest" in disaster_location[0]
            or "Southwest" in disaster_location[1]
        ):
            if "West" in disaster_location[0] or "West" in disaster_location[1]:
                return [x for x in disaster_location if "Southwest" not in x]
            return ["Empty"]
        if (
            "Southeast" in disaster_location[0]
            or "Southeast" in disaster_location[1]
        ):
            if (
                "South" in disaster_location[0]
                or "South" in disaster_location[1]
            ):
                return [x for x in disaster_location if "Southeast" not in x]
            return ["Empty"]
        if (
            "Northwest" in disaster_location[0]
            or "Northwest" in disaster_location[1]
        ):
            if "West" in disaster_location[0] or "West" in disaster_location[1]:
                return [x for x in disaster_location if "Northwest" not in x]
            return "Empty"
    if disaster_location:
        if disaster_location[0] == "Southeast":
            return "s"
        if disaster_location[0] == "Northwest":
            return "w"
        if disaster_location[0] == "Southwest":
            return "w"
        if disaster_location[0] == "Plains":
            return "m"
        else:
            return disaster_location[0]
    else:
        return "e"


def fill_one_region(dataframe, region_name):
    """
    docs
    """
    region_df = pd.DataFrame(
        columns=[
            "Name",
            "Disaster",
            "Begin Date",
            "End Date",
            "Total CPI-Adjusted Cost (Millions of Dollars)",
            "Deaths",
        ]
    )
    for _, row in dataframe.iterrows():
        if geo_locator(row["Name"]) == region_name:
            region_df.loc[len(region_df)] = row
    return region_df


def fill_all_regions(dataframe, region_list):
    """
    docs
    """
    df_list = {}
    for region_name in region_list:
        df_list[region_name] = fill_one_region(dataframe, region_name)
    return df_list


# these functions help us replace the unwieldy eight-character date format with
# the more general and more useful four-character year format
def parse_year(date):
    """
    Examines a given date in string form and returns only the year.

    Args:
        date: a string representing a specific date of a disaster.

    Returns: the first four characters of the date, representing the year.
    """
    return date[0:4]


def parse_all_years(dataframe):
    """
    Reformats the Begin Date and End Date columns of a dataframe to a
    four-character year format rather than an eight-character date format.

    Args:
        dataframe: a dataframe to reformat.

    Returns: None.
    """
    for col in ["Begin Date", "End Date"]:
        for i, date in dataframe[col].items():
            dataframe[i, col] = parse_year(date)


# these functions will get us unique lists of the columns we will sort by
def retrieve_unique_disaster_types(dataframe):
    """
    Returns a list of all different types of disasters within a given
    dataframe of disasters.

    Args:
        dataframe: a dataframe containing a list of disasters and their
        type designations.

    Returns: A list containing each unique disaster type.
    """
    return dataframe["Disaster"].unique()


def retrieve_unique_years(dataframe):
    """
    Returns a list of all different possible starting years out of a dataframe
    of different events.

    Args:
        dataframe: a dataframe containing a list of disasters and the dates
        that they occurred.

    Returns: A list containing each unique possible starting year.
    """
    start_years = []
    for event_row in dataframe.itertuples():
        print(event_row)
        start_years += parse_year(event_row.iloc([0]))
    return list(set(start_years))


# these split functions can be used to get yearly and disasterly dataframes
def generic_split_data(dataframe, split_by, child_group_set):
    """
    function that takes a dataframe of information and splits it into
    multiple child dataframes based on information in a particular
    column.

    Args:
    split_by: a string representing the column containing the information
    with which to split up the dataframe.
    child_group_set: a list representing the groups of data that each child
    dataframe will contain.

    Returns: A list of child dataframes that are each distinct from each
    other in some particular column.
    """
    subframe_dict = {}
    for subframe_cat in child_group_set:
        subframe = dataframe[dataframe[split_by] == subframe_cat]
        subframe_dict[subframe_cat] = subframe
    return subframe_dict


def split_by_year(dataframe):
    """
    Function that takes a dataframe and splits it into multiple child
    dataframes by disaster starting year.

    Args:
        dataframe: a dataframe containing dated disasters. Note: this function
        assumes that the dates here will be four-character years, NOT the
        original eight-character specific date format.

    Returns: A list of child dataframes, each associated with a particular
    start year.
    """
    return generic_split_data(
        dataframe, "Begin Date", retrieve_unique_years(dataframe)
    )


def split_by_disaster(dataframe):
    """
    Function that takes a dataframe and splits it into multiple child
    dataframes by disaster type.

    Args:
        dataframe: a dataframe containing disasters and their types.

    Returns: A list of child dataframes, each associated with a particular
    type of disaster.
    """
    return generic_split_data(
        dataframe, "Disaster", retrieve_unique_disaster_types(dataframe)
    )


# the following sum functions can be used for each step of summing.
def generic_sum_by_type(dataframe, disaster_type, desired_sum):
    """
    Given a frame of data and a particular type of disaster, comb through
    each event of the supplied type and sum up a desired value about them.

    Args:
        dataframe: the dataframe to parse.
        disaster_type: a string representing the type of disaster to look for.
        desired_sum: a string representing the numerical value to sum up
        across disasters.
    Returns:
        An int representing the sum of the requested value for all of the
        disasters of a certain type within the supplied dataframe.
    """
    sum_value = 0
    for _, event in dataframe.iterrows():
        if event["Disaster"] == disaster_type:
            sum_value += int(event[desired_sum])
    return sum_value


def death_by_sum(dataframe, disaster_type):
    """
    Given a frame of data and a particular type of disaster, comb through
    each event of the supplied type and sum up their total death count.

    Args:
        dataframe: the dataframe to parse.
        disaster_type: a string representing the type of disaster to look for.
    Returns:
        An int representing the sum of the total deaths for all of the
        disasters of a certain type within the supplied dataframe.
    """
    return generic_sum_by_type(dataframe, disaster_type, "Deaths")


def cost_by_sum(dataframe, disaster_type):
    """
    Given a frame of data and a particular type of disaster, comb through
    each event of the supplied type and sum up their total CPI-adjusted
    cost.

    Args:
        dataframe: the dataframe to parse.
        disaster_type: a string representing the type of disaster to look for.
    Returns:
        An int representing the sum of the CPI-adjusted cost for all of the
        disasters of a certain type within the supplied dataframe.
    """
    return generic_sum_by_type(
        dataframe,
        disaster_type,
        "Total CPI-Adjusted Cost (Millions of Dollars)",
    )
