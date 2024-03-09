import data_fetch
import data_process

data_fetch.write_to_csv()
disaster_data = data_process.read_csv_to_var(
    "./0209268/17.17/data/0-data/events-US-1980-2023.csv"
)
print(disaster_data)
