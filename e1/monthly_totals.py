import numpy as np
import pandas as pd


def get_precip_data():
    """
    Reads precipitation data from 'precipitation.csv'.
    The 'date' column (index 2) is parsed into datetime objects.
    """
    try:

        df = pd.read_csv('precipitation.csv', parse_dates=[2])

        return df
    except FileNotFoundError:
        print("Error: 'precipitation.csv' not found. Make sure the file is in the correct directory.")
        raise
    except Exception as e:
        print(f"Error reading or parsing 'precipitation.csv': {e}")
        print("Please ensure 'precipitation.csv' is correctly formatted and the date column (index 2) can be parsed.")
        raise


def date_to_month(d):
    """
    Converts a datetime object to a 'YYYY-MM' string.
    From monthly_totals_hint.py.
    """
    # You may need to modify this function, depending on your data types.
    # This function expects 'd' to be a datetime object with .year and .month attributes.
    return '%04i-%02i' % (d.year, d.month)


def pivot_months_pandas(data):
    """
    Create monthly precipitation totals for each station in the data set.
    This should use Pandas methods to manipulate the data.
    """
    # The 'data' DataFrame comes from get_precip_data(), 
    # which should have parsed the 'date' column into datetime objects.
    
    df_copy = data.copy() # Work on a copy

    # 1. Add a 'month_col' column by applying the 'date_to_month' function.
    # This assumes 'date' is the name of the column containing datetime objects.
    try:
        df_copy['month_col'] = df_copy['date'].apply(date_to_month)
    except KeyError:
        print("Error: Column 'date' not found in the DataFrame from get_precip_data().")
        print("Please ensure get_precip_data() provides a DataFrame with a 'date' column of datetime objects.")
        raise
    except AttributeError:
        print("Error: The 'date' column does not seem to contain datetime objects as expected by date_to_month.")
        print("Please check get_precip_data() and the 'date' column type.")
        raise


    # 2. Group by station 'name' and 'month_col', then aggregate.
    totals_aggregated = df_copy.groupby(['name', 'month_col']).aggregate(
        precipitation_sum=('precipitation', 'sum')
    ).reset_index()
    
    counts_aggregated = df_copy.groupby(['name', 'month_col']).aggregate(
        observation_count=('precipitation', 'count')
    ).reset_index()
    
    # 3. Pivot the aggregated dataframes.
    monthly = totals_aggregated.pivot(
        index='name', 
        columns='month_col',
        values='precipitation_sum'
    )
    
    counts = counts_aggregated.pivot(
        index='name', 
        columns='month_col',
        values='observation_count'
    )

    # 4. Fill missing values (NaNs) with 0.
    monthly.fillna(0, inplace=True)
    counts.fillna(0, inplace=True)
    
    # Sort columns (months) for consistent output.
    monthly = monthly.sort_index(axis=1)
    counts = counts.sort_index(axis=1)

    # Match column name style from pivot_months_loops for consistency.
    monthly.columns.name = 'month'
    counts.columns.name = 'month'
    
    return monthly, counts


def pivot_months_loops(data):
    """
    Create monthly precipitation totals for each station in the data set.
    This does it the hard way: using Pandas as a dumb data store, and iterating in Python.
    (Content from monthly_totals_hint.py)
    """
    # Find all stations and months in the data set.
    stations = set()
    months = set()
    for i,r in data.iterrows(): # This uses loops, as intended for this function
        stations.add(r['name'])
        # Assuming 'date' column exists and contains datetime objects
        m = date_to_month(r['date'])
        months.add(m)

    # Aggregate into dictionaries so we can look up later.
    stations = sorted(list(stations))
    # row_to_station = dict(enumerate(stations)) # Not used directly in DataFrame creation
    station_to_row = {s: i for i,s in enumerate(stations)}
    
    months = sorted(list(months))
    # col_to_month = dict(enumerate(months)) # Not used directly
    month_to_col = {m: i for i,m in enumerate(months)}

    # Create arrays for the data, and fill them.
    
    precip_total = np.zeros((len(stations), len(months)), dtype=float) # Use float for precipitation sums
    obs_count = np.zeros((len(stations), len(months)), dtype=int) # Use int for counts

    for _, row in data.iterrows(): # This uses loops
        m = date_to_month(row['date'])
        r_idx = station_to_row[row['name']]
        c_idx = month_to_col[m]

        precip_total[r_idx, c_idx] += row['precipitation']
        obs_count[r_idx, c_idx] += 1

    # Build the DataFrames we needed all along (tidying up the index names while we're at it).
    totals_df = pd.DataFrame(
        data=precip_total,
        index=stations,
        columns=months, # Use the sorted list of unique months found in the data
    )
    totals_df.index.name = 'name'
    totals_df.columns.name = 'month' # As per hint
    
    counts_df = pd.DataFrame(
        data=obs_count,
        index=stations,
        columns=months, # Use the sorted list of unique months
    )
    counts_df.index.name = 'name'
    counts_df.columns.name = 'month' # As per hint
    
    return totals_df, counts_df


def main():
    """
    Main function to load data, process it using pivot_months_pandas,
    and save the results.
    """
    print("Loading precipitation data...")
    try:
        data_df = get_precip_data()
    except Exception as e:
        # get_precip_data now raises errors, so we can stop if it fails.
        print(f"Stopping due to error in get_precip_data: {e}")
        return

    # As per exercise instructions: "When you submit, make sure your code is
    # using the pivot_months_pandas function you wrote."
    print("Processing data with pivot_months_pandas...")
    try:
        totals, counts = pivot_months_pandas(data_df)
    except Exception as e:
        print(f"Error during pivot_months_pandas: {e}")
        return

    # Save the recreated files
    try:
        print("Saving totals.csv...")
        totals.to_csv('totals.csv')

        print("Saving counts.csv...")
        counts.to_csv('counts.csv')

        print("Saving monthdata.npz...")
        # .values converts the DataFrame to a NumPy array.
        # Column order is preserved from the DataFrame.
        np.savez('monthdata.npz', totals=totals.values, counts=counts.values)
        print("Files saved successfully.")
    except Exception as e:
        print(f"Error saving files: {e}")

if __name__ == '__main__':
    main()
