"""
Functions that graph pre-processed data.
"""

import pandas as pd


def plot_dataframe(dataframe):
    """
    Plots a region dataframe.
    """
    dataframe.plot.bar(rot=90, stacked=True)


def test_plot():
    """
    fjkdfkk
    """
    speed = [0.1, 17.5, 40, 48, 52, 69, 88]

    lifespan = [2, 8, 70, 1.5, 25, 12, 28]

    index = ["snail", "pig", "elephant", "rabbit", "giraffe", "coyote", "horse"]

    df = pd.DataFrame({"speed": speed, "lifespan": lifespan}, index=index)

    return df


def plottable_by_time(region_dict, region_name, year_buckets):
    """
    Works for both cost and deaths! This function creates a dataframe
    representing data of ONE region for the purposes of plotting its
    damages with respect to time. This function will be used for each
    region so we can see how each of their costs changes with time.

    Args:
        region_dict: A dictionary of regions in which the key is the name
        of a region and the value is a dictionary of disasters and their
        damages across each unit of time.
        region_name: A string representing the name of a particular region
        whose data will be copied into a plottable dataframe.

    Returns: A dataframe that can be easily plotted such that the x-axis
    is in years and the y-axis is damages (cost or deaths works).
    """
    disasters_dict = region_dict[region_name]
    print(disasters_dict)
    plottable_df = pd.DataFrame.from_dict(disasters_dict)
    plottable_df.index = year_buckets
    return plottable_df


def plottable_by_region(region_dict, drs):
    """
    Works for both cost and deaths! This function creates a dataframe
    representing data of ALL regions, ignoring time, for the purpose of
    plottting each region's total damages across disaster types. This
    function will be used only once per damage type, so we can compare
    the sum damages between regions.

    Args:
        region_dict: A dictionary of regions in which the key is the name
        of a region and the value is a dictionary of disasters and their
        damages across each unit of time.
        drs: A list of all possible disaster types.

    Returns: A dataframe that can be easily plotted such that the x-axis
    shows regions and the y-axis is damages (cost or deaths works).
    """
    regions_sums = {}
    for region_name, region_val in region_dict.items():
        region_damage_list = []
        for _, disaster_damages in region_val.items():
            region_damage_list.append(sum(disaster_damages))
        regions_sums[region_name] = region_damage_list
    plottable_df = pd.DataFrame.from_dict(
        regions_sums, orient="index", columns=drs
    )
    return plottable_df
