import numpy as np
import matplotlib.pyplot as plt

# Load the data from monthdata.npz

try:
    data = np.load('monthdata.npz')
    totals = data['totals']  # Precipitation totals (rows: cities, columns: months)
    counts = data['counts']  # Observation counts (rows: cities, columns: months)
except FileNotFoundError:
    print("Error: 'monthdata.npz' not found. Make sure the file is in the correct directory.")
    exit()

# 1. Which city had the lowest total precipitation over the year?
# Sum precipitation across months for each city (axis=1)
total_precipitation_per_city = totals.sum(axis=1)
# Find the index (row number) of the city with the minimum sum
lowest_precip_city_index = total_precipitation_per_city.argmin()
print("Row with lowest total precipitation:")
print(lowest_precip_city_index)

# 2. Determine the average precipitation in these locations for each month.
# Sum totals for each month (axis=0), sum counts for each month (axis=0)
sum_totals_per_month = totals.sum(axis=0)
sum_counts_per_month = counts.sum(axis=0)

# Element-wise division.
# Handle potential division by zero if sum_counts_per_month can contain zeros.
average_precipitation_per_month = np.divide(
    sum_totals_per_month,
    sum_counts_per_month,
    out=np.zeros_like(sum_totals_per_month, dtype=float), # Output 0 where division is by zero
    where=sum_counts_per_month != 0
)
print("Average precipitation in each month:")
print(average_precipitation_per_month)

# 3. Do the same for the cities: average precipitation (daily precipitation averaged over the month) for each city.
# Calculate daily average for each city-month: totals / counts
# Handle potential division by zero.
daily_avg_precip_city_month = np.divide(
    totals,
    counts,
    out=np.zeros_like(totals, dtype=float), # Output 0 where division is by zero
    where=counts != 0
)
# Then average these daily averages across the months for each city (axis=1)
# If zeros from the division (where counts were 0) should be ignored in the mean,
# then np.nanmean should be used after converting those zeros to NaN.


daily_avg_precip_city_month_with_nan = np.divide(
    totals.astype(float), # Ensure float division
    counts.astype(float),
    out=np.full_like(totals, np.nan, dtype=float), # Output NaN where division is by zero
    where=counts != 0
)
average_daily_precip_per_city = np.nanmean(daily_avg_precip_city_month_with_nan, axis=1)
print("Average precipitation in each city:")
print(average_daily_precip_per_city)


# 4. Calculate the total precipitation for each quarter in each city.
# totals shape is (num_cities, 12 months)
# Reshape to (num_cities, 4 quarters, 3 months_per_quarter)
num_cities = totals.shape[0]
# Assuming totals.shape[1] is always 12 (as stated in the problem)
reshaped_totals = totals.reshape(num_cities, 4, 3)
# Sum across the 3 months for each quarter (axis=2)
quarterly_precipitation_per_city = reshaped_totals.sum(axis=2)
print("Quarterly precipitation totals:")
print(quarterly_precipitation_per_city)