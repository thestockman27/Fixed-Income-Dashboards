import sqlite3
import pandas as pd
import quandl
import numpy as np
from datetime import datetime
import warnings
# https://docs.data.nasdaq.com/docs/parameters-2#section-times-series-parameters

# Function to update a table with new data
def update_table(prefix,series_code, periodicity, conn, cursor):
    full_series_code = prefix + series_code
    table_name = series_codes[series_code] + '_' + periodicity
    # Print the list of existing tables
    existing_tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
    existing_tables = cursor.execute(existing_tables_query).fetchall()
    # print("Existing Tables:", [table[0] for table in existing_tables])

    # Check the latest date in the existing table
    query_latest_date = f'SELECT MAX(Date) FROM "{table_name}"'  # Use double quotes for table name
    latest_date = pd.read_sql_query(query_latest_date, conn).iloc[0, 0]

    # Fetch existing data from the database
    existing_data_query = f'SELECT * FROM "{table_name}"'
    existing_data = pd.read_sql_query(existing_data_query, conn)
    # Ensure numeric data types in existing data
    existing_data_numeric = existing_data.apply(pd.to_numeric, errors='coerce')
    existing_data_numeric = existing_data_numeric.dropna()
  
    # Fetch new data from Quandl if available
    new_data = quandl.get(full_series_code, collapse=periodicity, start_date=latest_date)

    if not new_data.empty:
        # Safety checks
        if new_data.isnull().values.any():
            print(f"Warning: Missing values found in {table_name}. Skipping update.")
            return

        expected_data_types = [np.float64]
        if not all(pd.api.types.is_numeric_dtype(dtype) for dtype in new_data.dtypes):
            print(f"Warning: Incorrect data types found in {table_name}.")
            print(f"Expected data types: {expected_data_types}")
            print(f"Actual data types: {new_data.dtypes}")
            print("Proceeding with the update.")

        # Calculate IQR from existing data
        Q1_existing = existing_data_numeric.quantile(0.25)
        Q3_existing = existing_data_numeric.quantile(0.75)
        IQR_existing = Q3_existing - Q1_existing

        # Get the intersection of columns
        common_columns = new_data.columns.intersection(existing_data_numeric.columns)

        # Identify outliers using the IQR method on common columns
        outliers = (
            (new_data[common_columns] < (Q1_existing[common_columns] - 1.5 * IQR_existing[common_columns])) |
            (new_data[common_columns] > (Q3_existing[common_columns] + 1.5 * IQR_existing[common_columns]))
        ).any(axis=1)
        if outliers.any():
            warnings.warn(f"Warning: Outliers found in {table_name}. Proceeding with the update.")

        # Check for duplicate date observations
        if latest_date is not None and new_data.index.max() <= pd.to_datetime(latest_date):
            print(f"No new data available for {table_name}.")
        else:
           # Append new observations to the original table
            new_observations = new_data[new_data.index > pd.to_datetime(latest_date)]
            new_observations.to_sql(table_name, conn, if_exists='append', index=True)
            # Create a table for the period-to-period difference
            diff_data = new_data.diff().dropna()
            diff_table_name = table_name + '_diff'
            diff_data.to_sql(diff_table_name, conn, if_exists='append', index=True)

            # Create a table for the percent change with handling of Inf values
            percent_change_data = new_data.pct_change().dropna()
            percent_change_table_name = table_name + '_percent_change'
            percent_change_data.to_sql(percent_change_table_name, conn, if_exists='append', index=True)

            print(f"Updated {table_name} with new data.")
    else:
        print(f"No new data available for {table_name}.")
