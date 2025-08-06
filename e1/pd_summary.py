import pandas as pd
import numpy as np

# Load data from CSV and set the 'name' column as the index.
try:
    totals = pd.read_csv('totals.csv').set_index(keys=['name'])
    counts = pd.read_csv('counts.csv').set_index(keys=['name'])
except FileNotFoundError as e:
    print(f"Error: {e}. Make sure totals.csv and counts.csv are in the correct directory.")
    raise

# 1. Which city had the lowest total precipitation over the year?
total_precipitation_per_city = totals.sum(axis=1)
lowest_precip_city_name = total_precipitation_per_city.idxmin()
print("City with lowest total precipitation:")
print(lowest_precip_city_name)


# 2. Determine the average precipitation in these locations for each month.
sum_totals_per_month = totals.sum(axis=0)
sum_counts_per_month = counts.sum(axis=0)
average_precipitation_per_month = sum_totals_per_month / sum_counts_per_month
print("Average precipitation in each month:")
print(average_precipitation_per_month)



# Calculate the total precipitation for the entire year for each city.
total_yearly_precip = totals.sum(axis=1)

# Calculate the total number of observation days for the entire year for each city.
total_yearly_counts = counts.sum(axis=1)

# Divide the total yearly precipitation by the total yearly observation days
# to get the overall average daily precipitation for the year.
average_daily_precip_per_city = total_yearly_precip / total_yearly_counts

print("Average precipitation in each city:")
print(average_daily_precip_per_city)