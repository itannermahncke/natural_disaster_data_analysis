"""
Test the functions in process_data.py

Imports:
pytest to write pytests!
pandas to write dataframes for the pytests!

Things to note:
Testing the fill_all_regions function would look like copying the
fill_one_region tests, but switching the "Western" part of the test to
["Western", "Southern", "Midwestern", "Northeastern"] because it takes
a list instead of the name of one region.

Testing the generic_split_data function is a task that is unwieldy by nature
and gets tested by larger functions that call it, so those will be tested
instead.

Testing the split_by_year, split_by_disaster, death_by_sum, and cost_by_sum
functions simply involves calling the generic_split_data and
generic_sum_by_type with one extra parameter specified and are not worth the
extra tests, especially because those functions are called by other larger
functions that will be tested anyway.

Testing assemble_one_disaster is something that happens as a result of testing
assemble_region_data.

Testing the organize_regions function is not the best use of time because
it calls other functions that are being tested in a for loop.
"""

import pytest
import pandas as pd

from process_data import (
    parse_year,
    retrieve_unique_disaster_types,
    geo_locator,
    fill_one_region,
    generic_sum_by_type,
    sum_years_in_buckets,
    assemble_region_data,
)


# Define sets of test cases.
parse_year_cases = [
    # Check empty.
    ("", ""),
    # Check that the function functions as expected.
    ("20250000", "2025"),
]

disaster_type_cases = [
    # Check empty.
    (pd.DataFrame({"Disaster": [""]}), [""]),
    # Check that the function functions as expected.
    (pd.DataFrame({"Disaster": ["a", "b", "c"]}), ["a", "b", "c"]),
    (pd.DataFrame({"Disaster": ["a", "b", "b", "c", "c"]}), ["a", "b", "c"]),
]

# Define sets of test cases.
geo_locator_cases = [
    # Check empty.
    ("", "empty"),
    # Check other cases that should return empty.
    ("20250000", "empty"),
    ("Northeast South Midwest West", "empty"),
    ("Minnessota", "empty"),
    # Check that the function functions as expected.
    ("Houston", "Southern"),
    ("Northwest", "Western"),
    ("Minnesota", "Midwestern"),
    ("Bob", "Northeastern"),
    # Check the two "hardcoded" special cases
    ("North/Central Texas Hail Storm (April 2016)", "Southern"),
    ("North Texas Hail Storm (March 2016)", "Southern"),
]

fill_one_region_cases = [
    # Check empty dataframe.
    (
        pd.DataFrame(
            {
                "Name": [""],
                "Disaster": [""],
                "Begin Date": [""],
                "End Date": [""],
                "Total CPI-Adjusted Cost (Millions of Dollars)": [""],
                "Deaths": [""],
            }
        ),
        "Western",
        pd.DataFrame(
            columns=[
                "Name",
                "Disaster",
                "Begin Date",
                "End Date",
                "Total CPI-Adjusted Cost (Millions of Dollars)",
                "Deaths",
            ]
        ),
    ),
    # Check that the function functions as expected.
    (
        pd.DataFrame(
            {
                "Name": ["West Storm"],
                "Disaster": ["Storm"],
                "Begin Date": ["1"],
                "End Date": ["2"],
                "Total CPI-Adjusted Cost (Millions of Dollars)": ["3"],
                "Deaths": ["4"],
            }
        ),
        "Western",
        pd.DataFrame(
            {
                "Name": ["West Storm"],
                "Disaster": ["Storm"],
                "Begin Date": ["1"],
                "End Date": ["2"],
                "Total CPI-Adjusted Cost (Millions of Dollars)": ["3"],
                "Deaths": ["4"],
            }
        ),
    ),
    (
        pd.DataFrame(
            {
                "Name": ["West Storm"],
                "Disaster": ["Storm"],
                "Begin Date": ["1"],
                "End Date": ["2"],
                "Total CPI-Adjusted Cost (Millions of Dollars)": ["3"],
                "Deaths": ["4"],
            }
        ),
        "Southern",
        pd.DataFrame(
            columns=[
                "Name",
                "Disaster",
                "Begin Date",
                "End Date",
                "Total CPI-Adjusted Cost (Millions of Dollars)",
                "Deaths",
            ]
        ),
    ),
]

generic_sum_by_type_cases = [
    # Check empty.
    (pd.DataFrame({"Numbers": []}), "Numbers", 0),
    # Check that the function functions as expected.
    (pd.DataFrame({"Numbers": [1, 2, 3]}), "Numbers", 6),
]

sum_years_in_buckets_cases = [
    # Check empty.
    ([], 2, []),
    # Check that the function functions as expected.
    ([1, 2, 3, 4], 2, [3, 7]),
]

assemble_region_data_cases = [
    # Check some empty cases.
    (
        pd.DataFrame(
            {
                "Disaster": [""],
            }
        ),
        ["Storm"],
        [1, 2, 3, 4],
        2,
        ({1: [0], 2: [0], 3: [0], 4: [0]}, {1: [0], 2: [0], 3: [0], 4: [0]}),
    ),
    (
        pd.DataFrame(
            {
                "Disaster": ["Storm", "Fire", "Storm", "Flood"],
                "Deaths": [10, 5, 20, 3],
                "Total CPI-Adjusted Cost (Millions of Dollars)": [1, 2, 3, 4],
            }
        ),
        ["Storm"],
        [],
        2,
        ({}, {}),
    ),
]


# Define standard testing functions to check functions' outputs given certain
# inputs defined above.
@pytest.mark.parametrize("date,year", parse_year_cases)
def test_parse_year(date, year):
    """
    Given a date made up of a bunch of number characters in a row, check
    that the function correctly maps to a year of only the first four numbers.
    Also check that it handles an empty value appropriately.

    Args:
        date: A string with a date made up of numbers
        year: A string with four numbers that represent a year.
    """
    result = parse_year(date)
    assert isinstance(result, str)
    assert result == year


@pytest.mark.parametrize("dataframe,disaster_list", disaster_type_cases)
def test_retrieve_unique_disaster_types(dataframe, disaster_list):
    """
    Given a dataframe, check that the function correctly maps to a list
    of strings which are the unique items from the dataframe. Also check that
    it handles an empty value appropriately.

    Args:
        dataframe: A dataframe with names of natural disasters.
        disaster_list: A list of strings with names of natural disasters.

    """
    result = retrieve_unique_disaster_types(dataframe)
    assert result.tolist() == disaster_list


@pytest.mark.parametrize("disaster_name,region", geo_locator_cases)
def test_geo_locator(disaster_name, region):
    """
    Given a string with a short description of a disaster, check that the
    function correctly maps to a string which is the region the disaster
    affects. Also check that it handles an empty value appropriately.

    Args:
        disaster_name: A string with a description of the natural disaster.
        region: A string with the name of a region in the U.S.
    """
    result = geo_locator(disaster_name)
    assert isinstance(result, str)
    assert result == region


@pytest.mark.parametrize(
    "dataframe,region_name,region_disasters", fill_one_region_cases
)
def test_fill_one_region(dataframe, region_name, region_disasters):
    """
    Given a dataframe and a string with a U.S. region, check that the
    function correctly maps to a dataframe which has all the disasters that
    have affected the region. Also check that it handles an empty value
    appropriately.

    Args:
        dataframe: A dataframe with disaster descriptions, names, dates, cost,
        and deaths.
        region_name: A string with the name of a region in the U.S.
        region_disasters: A dataframe with all of the natural disasters that
        have affected the region.
    """
    result = fill_one_region(dataframe, region_name)
    assert ((result == region_disasters).all()).all()


@pytest.mark.parametrize(
    "dataframe,desired_sum,total", generic_sum_by_type_cases
)
def test_generic_sum_by_type(dataframe, desired_sum, total):
    """
    Given a dataframe and a string with the name of a column in the dataframe,
    check that the function correctly maps to the sum of all values in that
    column. Also check that it handles an empty value appropriately.

    Args:
        dataframe: A dataframe with disaster descriptions, names, dates, cost,
        and deaths.
        desired_sum: A string with the name of one of the dataframe columns.
        total: A float that is the sum of the specified dataframe column.
    """
    result = generic_sum_by_type(dataframe, desired_sum)
    assert isinstance(result, float)
    assert result == total


@pytest.mark.parametrize(
    "num_list,bucket_size,regrouped_list", sum_years_in_buckets_cases
)
def test_sum_years_in_buckets(num_list, bucket_size, regrouped_list):
    """
    Given a list of ints which are a set of years and an int representing
    bucket size, check that the function correctly maps to a list of ints that
    is the size of num_list divided by bucket_size. Also check that it handles
    an empty value appropriately.

    Args:
        num_list: A list of ints which are a continuous set of years.
        bucket_size: An int with the bucket size.
        regrouped_list: A list of integers of a certain length.
    """
    result = sum_years_in_buckets(num_list, bucket_size)
    assert result == regrouped_list


@pytest.mark.parametrize(
    "dataframe,yrs,drs,yr_buckets,dictionaries", assemble_region_data_cases
)
def test_assemble_region_data(dataframe, yrs, drs, yr_buckets, dictionaries):
    """
    Given a dataframe, a list of ints which are a set of years, a list of all
    disasters in the dataframe, and an int representing the bucket size as per
    the previous test, check that the function handles empty values
    appropriately by returning dictionaries (one for costs, one for deaths)
    that are empty or hold keys that map to zeros.

    Args:
        dataframe: A dataframe with disaster descriptions, names, dates, cost,
        and deaths.
        yrs: A list of ints which are a continuous set of years.
        drs: A list of disasters which are found in the dataframe.
        yr_buckets: An int with the bucket size.
        dictionaries: Dictionaries for costs and deaths in the years listed and
        caused by the disasters listed.
    """
    result = assemble_region_data(dataframe, yrs, drs, yr_buckets)
    assert result == dictionaries
