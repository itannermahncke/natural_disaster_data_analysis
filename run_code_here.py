"""
File for testing code until we have a comp essay.
"""

import data_fetch
import data_process as dp

data_fetch.write_to_csv(
    "https://www.ncei.noaa.gov/archive/archive-management-system/OAS/bin/prd/jquery/download/209268.17.17.tar.gz",
    "209268.17.17.tar.gz",
)

region_list = ["w", "m", "s", "n", "empty"]

disaster_data = dp.read_csv_to_var(
    "./0209268/17.17/data/0-data/events-US-1980-2023.csv"
)

region_dict = dp.fill_all_regions(disaster_data, region_list)
print(region_dict)

READY = False

if READY:
    # for each region dataframe
    region_sorted_list = []
    for region_name, region_frame in region_dict.items():
        region_loaf = {}
        region_year_dict = dp.split_by_year(region_frame)
        # for each region-year dataframe, stack slices and append to region loaf
        for region_year_name, region_year_frame in region_year_dict.items():
            region_year_slice = []
            region_year_disaster_dict = dp.split_by_disaster(region_year_frame)
            # for each region-year-disaster, sum and append to region-year slice
            for (
                disaster_name,
                disaster_frame,
            ) in region_year_disaster_dict.items():
                # sum values
                sum_cost = dp.cost_by_sum(disaster_frame, disaster_name)
                sum_death = dp.death_by_sum(disaster_frame, disaster_name)
                # add data chunk to year slice
                region_year_slice.append([disaster_name, sum_cost, sum_death])
            region_loaf[region_year_name] = region_year_slice
        region_sorted_list.append(region_loaf)
