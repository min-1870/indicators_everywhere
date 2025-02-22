import yfinance as yf
from datetime import datetime, timedelta
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from src.app.constants import S3_GRAPHS_PATH, S3_BUCKET_NAME, DEBUG


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
    stock_data.columns = stock_data.columns.get_level_values(0)
    
    if len(stock_data) == 0:
        raise ValueError("Failed to fetch the finance history.")

    return stock_data


def upload_image_to_s3(graphs_directory, file_name):

    if not DEBUG:
        try:
            # Initialize the S3 client
            s3 = boto3.client("s3")

            local_directory = graphs_directory / file_name
            s3_directory = f"{S3_GRAPHS_PATH}{file_name}"

            # Upload the file
            s3.upload_file(
                local_directory,
                S3_BUCKET_NAME,
                s3_directory,
                ExtraArgs={
                    "ContentType": "image/png",
                },
            )

            if local_directory.exists():
                local_directory.unlink()

        except FileNotFoundError:
            print("The file was not found.")
        except NoCredentialsError:
            print("Credentials not available.")
        except PartialCredentialsError:
            print("Incomplete credentials provided.")
        except Exception as e:
            print(f"An error occurred: {e}")
