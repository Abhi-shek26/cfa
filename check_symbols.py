# This script checks the available stock symbols in the provided Parquet file.
import pandas as pd

try:
    # Make sure the filename matches yours
    df = pd.read_parquet('stocks_ohlc_data.parquet')
    
    # Get a list of all unique symbols
    symbols = df['symbol'].unique()
    
    print("--- Symbols available in your data file ---")
    for symbol in symbols:
        print(symbol)
    print("-----------------------------------------")

except FileNotFoundError:
    print("Error: Could not find 'stocks_ohlc_data.parquet'.")
    print("Please make sure the file is in the same directory as this script.")
except Exception as e:
    print(f"An error occurred: {e}")
    print("Please ensure you have pandas and pyarrow installed (`pip install pandas pyarrow`).")

