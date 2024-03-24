"""
Functions that graph pre-processed data.
"""

import pandas as pd


def create_plottable_region(region_dict, region_name):
    """
    Args:
        region_dict: A dictionary of regions in which the key is the name
        of a region and the value is a dictionary of year keys and 2d
        array values.
        region_name: The name of a particular region whose data will be
        copied into a plottable dataframe.

    Returns: A dataframe that can be easily plotted such that the x-axis
    is in years and the y-axis is in millions of dollars.
    """
    years_dict = region_dict[region_name]
    for year, year_2d_array in years_dict.items():
        # you want a list for each disaster
        # the number of items is equal to the number of years
        # if the disaster has no values for a year it should be zero
        continue
    # df = pd.DataFrame(data, columns=index)
    # return df


def plot_one_region(dataframe):
    """
    Plots a region dataframe.
    """
    dataframe.plot.bar(stacked=True)


def test_plot():
    """
    fjkdfkk
    """
    speed = [0.1, 17.5, 40, 48, 52, 69, 88]

    lifespan = [2, 8, 70, 1.5, 25, 12, 28]

    index = ["snail", "pig", "elephant", "rabbit", "giraffe", "coyote", "horse"]

    df = pd.DataFrame({"speed": speed, "lifespan": lifespan}, index=index)

    return df
