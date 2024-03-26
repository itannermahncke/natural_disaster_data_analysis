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
            dataframe[col].iloc[i - 1] = parse_year(date)


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

    Returns: A list containing each unique possible starting year in ascending
    order, as strings.
    """
    start_years = []
    year_column = dataframe["Begin Date"]
    for _, year in year_column.items():
        start_years.append(int(year))
    start_years.sort()
    unique_years = list(set(start_years))
    for i, year in enumerate(unique_years):
        unique_years[i] = str(year)
    return unique_years


# function that takes a disaster name and index and returns the region
# destination
def geo_locator(disaster_name):
    """
    docs
    """
    disaster_location = []
    south_set = [
        "South ",
        "Southern",
        "Southeast",
        "Southwest",
        "Florida",
        "Gulf ",
        "Virginia",
        "Texas",
        "Mississippi",
        "Georgia",
        "Houston",
        "Louisiana",
        "Arkansas",
        "Tennessee",
        "Kentucky",
        "Fort Lauderdale",
        "Oklahoma",
        "Virginia",
        "Mid-Atlantic",
        "Allen",
        "Alicia",
        "Elena",
        "Allison",
        "Hugo",
        "Andrew",
        "Alberto",
        "Erin",
        "Opal",
        "Fran",
        "Frances",
        "Bonnie",
        "Georges",
        "Floyd",
        "Lili",
        "Isidore",
        "Isabel",
        "Charley",
        "Ivan",
        "Jeanne",
        "Dennis",
        "Katrina",
        "Rita",
        "Wilma",
        "Dolly",
        "Gustav",
        "Ike",
        "Lee",
        "Isaac",
        "Matthew",
        "Harvey",
        "Irma",
        "Maria",
        "Florence",
        "Michael",
        "Dorian",
        "Imelda",
        "Hanna",
        "Isaias",
        "Laura",
        "Sally",
        "Delta",
        "Zeta",
        "Eta",
        "Elsa",
        "Fred",
        "Hurricane Ida",
        "Nicholas",
        "Fiona",
        "Hurricane Ian",
        "Nicole",
        "Idalia",
    ]
    west_set = [
        "West ",
        "Western",
        "Northwest",
        "Colorado",
        "California",
        "Oakland",
        "Rockies",
        "Arizona",
        "Alaska",
        "Hawaii",
        "Iniki",
    ]
    midwest_set = [
        "Midwest",
        "Central",
        "Plains",
        "Kansas",
        "Missouri",
        "Illinois",
        "Michigan",
        "Minnesota",
    ]
    northeast_set = [
        "Northeast",
        "New England",
        "Bob",
        "Irene",
        "Sandy",
    ]

    for s_key in south_set:
        if s_key in disaster_name:
            disaster_location.append("s")
            break
    for w_key in west_set:
        if w_key in disaster_name:
            disaster_location.append("w")
            break
    for m_key in midwest_set:
        if m_key in disaster_name:
            disaster_location.append("m")
            break
    for n_key in northeast_set:
        if n_key in disaster_name:
            disaster_location.append("n")
            break

    if (
        disaster_name in "North/Central Texas Hail Storm (April 2016)"
        or disaster_name in "North Texas Hail Storm (March 2016)"
    ):
        disaster_location.clear()
        disaster_location.append("s")

    if len(disaster_location) == 1:
        return disaster_location[0]
    return "empty"


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
def generic_sum_by_type(dataframe, desired_sum):
    """
    Given a frame of data, comb through each event and sum up a desired
    value about them.

    Args:
        dataframe: the dataframe to parse.
        desired_sum: a string representing the numerical value to sum up
        across disasters.
    Returns:
        An int representing the sum of the requested value for all of the
        disasters within the supplied dataframe.
    """
    sum_value = 0
    for _, event in dataframe.iterrows():
        sum_value += float(event[desired_sum])
    return sum_value


def death_by_sum(dataframe):
    """
    Given a frame of data, comb through each event of the supplied type
    and sum up their total death count.

    Args:
        dataframe: the dataframe to parse.
    Returns:
        An int representing the sum of the total deaths for all of the
        disasters of a certain type within the supplied dataframe.
    """
    return generic_sum_by_type(dataframe, "Deaths")


def cost_by_sum(dataframe):
    """
    Given a frame of data, comb through
    each event of the supplied type and sum up their total CPI-adjusted
    cost.

    Args:
        dataframe: the dataframe to parse.
    Returns:
        An int representing the sum of the CPI-adjusted cost for all of the
        disasters of a certain type within the supplied dataframe.
    """
    return generic_sum_by_type(
        dataframe,
        "Total CPI-Adjusted Cost (Millions of Dollars)",
    )


def assemble_one_disaster(dataframe, yrs):
    """
    Args:
        dataframe: A dataframe containing information of a single disaster
        type within a single region; the data spans all years.
        yrs: a list containing all possible years. For use in adding relevant
        zeroes where there is no data.

    Returns: Two arrays. One contains sum cost per year for the disaster type,
    the other contains sum deaths per year for the disaster type. The values
    are all floats.
    """
    # split by year
    years_dict = split_by_year(dataframe)
    cost_arr = []
    death_arr = []
    # for each year in unique years list
    for year in yrs:
        # if this disaster happened here this year
        if year in years_dict:
            # sum deaths, sum cost of the year for this disaster
            # append to disaster-specific array (cost and death separated)
            cost_arr.append(cost_by_sum(years_dict[year]))
            death_arr.append(death_by_sum(years_dict[year]))
        # if this disaster did not happen here this year
        else:
            # append zeroes as to not stagger the data
            cost_arr.append(0)
            death_arr.append(0)
    # now you have data across years for one disaster in one region
    return cost_arr, death_arr


def assemble_region_data(dataframe, yrs, drs):
    """
    Args:
        dataframe: a dataframe containing information of all disasters across
        all years within a single US region.
        yrs: a list containing all possible years. This will be carried to the
        deepest function for use in adding relevant zeroes where there is no
        data.
        drs: a list containing all possible disasters. For use in adding
        relevant zeroes where there is no data.

    Returns: Two dictionaries, one for cost and one for deaths. In both, the
    keys are disaster types and the values are arrays containing by-the-year
    data on sum damages (cost or deaths respectively).
    """
    # this code is for one region
    organized_disasters_cost = {}
    organized_disasters_deaths = {}
    # split up by disaster first
    disasters_dict = split_by_disaster(dataframe)
    # for each disaster in disasters list
    for disaster in drs:
        # if this region has experienced this disaster
        if disaster in disasters_dict:
            cost_arr, death_arr = assemble_one_disaster(
                disasters_dict[disaster], yrs
            )
            organized_disasters_cost[disaster] = cost_arr
            organized_disasters_deaths[disaster] = death_arr
        # if this region has not experienced this disaster
        else:
            # fill this disaster key's value with zeroes for every year
            zeroes = [0] * len(yrs)
            organized_disasters_cost[disaster] = zeroes
            organized_disasters_deaths[disaster] = zeroes
    # now you have data across years for all disasters in one region
    return organized_disasters_cost, organized_disasters_deaths


def organize_regions(region_dict, yrs, drs):
    """
    A function that takes a dictionary containing regional data and returns
    that data sorted such that it is easily plottable by year, disaster type,
    and region.

    Args:
        region_dict: a dictionary in which the keys are the names of US regions
        and the values are dataframes containing their unorganized values.
        yrs: a list containing all possible years. This will be carried to the
        deepest function for use in adding relevant zeroes where there is no
        data.
        drs: a list containing all possible disasters. This will be carried to
        the deepest function for use in adding relevant zeroes where there is no
        data.

    Returns: A list containing two dictionaries; one for cost and deaths
    respectively. Each is a dictionary in which the keys are the names of US
    regions and the values are dictionaries in which the keys are disaster
    types and the values are arrays containing information on sum damages
    (cost or deaths) of that disaster type for each year.
    """
    regions_sorted_cost = {}
    regions_sorted_deaths = {}
    for region_name, region_frame in region_dict.items():
        region_as_cost, region_as_deaths = assemble_region_data(
            region_frame, yrs, drs
        )
        regions_sorted_cost[region_name] = region_as_cost
        regions_sorted_deaths[region_name] = region_as_deaths
    return regions_sorted_cost, regions_sorted_deaths
