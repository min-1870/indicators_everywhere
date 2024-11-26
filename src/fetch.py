import yfinance as yf
from datetime import datetime, timedelta

def fetch_data(symbol, duration):
    """
    This function fetch history prices of a stock from yahoo finance.
    """
    
    # Get the current date
    current_date = datetime.now()

    # Define the start and end dates
    start_date = (current_date - timedelta(days=duration)).strftime("%Y-%m-%d")

    # Format the date as a string in the desired format
    end_date = current_date.strftime("%Y-%m-%d")

    # Fetch historical data with a daily interval
    stock_data = yf.download(symbol, start=start_date, end=end_date, interval="1d")

    if len(stock_data) == 0:
        raise ValueError("Failed to fetch the finance history.")

    return stock_data
