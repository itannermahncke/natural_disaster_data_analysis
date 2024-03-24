"""
File for testing code until we have a comp essay.
"""

import data_fetch
import data_process as dp
import data_graph as dg

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
