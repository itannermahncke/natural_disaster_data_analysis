"""
File for testing code until we have a comp essay.
"""

import data_fetch
import data_process as dp

# establish universal regions, plus a scrap bin
region_list = ["w", "m", "s", "n", "empty"]

# request dataset from online and store it in a variable
# data_fetch.write_to_csv(
# "https://www.ncei.noaa.gov/archive/archive-management-system/OAS/bin/prd/jquery/download/209268.17.17.tar.gz",
# "209268.17.17.tar.gz",
# )
disaster_data = dp.read_csv_to_var(
    "./0209268/17.17/data/0-data/events-US-1980-2023.csv"
)

# modify dates to be less specific years
dp.parse_all_years(disaster_data)

# log the disaster types and years found in the dataset
unique_types = dp.retrieve_unique_disaster_types(disaster_data)
unique_years = dp.retrieve_unique_years(disaster_data)

# convert the raw data (sorted by region) into graphable blocks of data
region_dict = dp.fill_all_regions(disaster_data, region_list)
sorted_data_dict = dp.organize_all_regions(region_dict)
