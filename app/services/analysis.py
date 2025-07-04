import pandas as pd
import pandas_ta as ta
from functools import lru_cache
from app.core.config import settings

# This module provides functions to calculate technical indicators for stock data.
@lru_cache(maxsize=1)

# Load stock data from the parquet file
def load_stock_data():
    """Loads stock data from the parquet file.
    Uses lru_cache to ensure the data is loaded from disk only once."""
    try:
        df = pd.read_parquet(settings.STOCK_DATA_PATH)
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        return df
    except FileNotFoundError:
        # In a real application, you'd have more robust error handling/logging
        print(f"Error: The data file was not found at {settings.STOCK_DATA_PATH}")
        return pd.DataFrame()

# This function calculates a specific technical indicator for a given stock symbol and date range.
def get_technical_indicator(symbol: str, indicator: str, start_date: str, end_date: str, **kwargs):
    """
    Calculates a single technical indicator for a given stock symbol and date range.
    """
    df = load_stock_data()
    if df.empty or symbol not in df['symbol'].unique():
        return None

    stock_df = df[df['symbol'] == symbol].copy()
    stock_df = stock_df.loc[start_date:end_date]

    if stock_df.empty:
        return None
        
    indicator_series = None

    # Using pandas_ta for calculations
    if indicator.lower() == 'sma':
        indicator_series = stock_df.ta.sma(length=kwargs.get('period', 20))
    elif indicator.lower() == 'ema':
        indicator_series = stock_df.ta.ema(length=kwargs.get('period', 20))
    elif indicator.lower() == 'rsi':
        indicator_series = stock_df.ta.rsi(length=kwargs.get('period', 14))
    elif indicator.lower() == 'macd':
        # MACD returns a DataFrame with multiple columns
        macd_df = stock_df.ta.macd(fast=kwargs.get('fast', 12), slow=kwargs.get('slow', 26), signal=kwargs.get('signal', 9))
        indicator_series = macd_df['MACD_12_26_9'] # We'll return just the MACD line for simplicity
    elif indicator.lower() == 'bollinger':
        # Bollinger Bands also returns a DataFrame
        bb_df = stock_df.ta.bbands(length=kwargs.get('period', 20), std=kwargs.get('std_dev', 2))
        indicator_series = bb_df['BBM_20_2.0'] # We'll return the middle band
    
    if indicator_series is None or indicator_series.empty:
        return []

    # Format for response
    results = []
    for date, value in indicator_series.items():
        results.append({
            "date": date.strftime('%Y-%m-%d'),
            "value": None if pd.isna(value) else round(value, 2)
        })

    return results
