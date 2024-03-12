"""
File for testing code until we have a comp essay.
"""

import data_fetch
import data_process

data_fetch.write_to_csv(
    "https://www.ncei.noaa.gov/archive/archive-management-system/OAS/bin/prd/jquery/download/209268.17.17.tar.gz",
    "209268.17.17.tar.gz",
)
disaster_data = data_process.read_csv_to_var(
    "./0209268/17.17/data/0-data/events-US-1980-2023.csv"
)

i = 0
for index in disaster_data:
    print(data_process.geo_locator(index[0], i))
    i += 1

# 1) split dataframe into regions
# 2) for each region, split into yearly data
# 3) for each region-year, split into disaster data
