from src.app.constants import US_STOCK_FILE_NAME
from pathlib import Path
import json
import random


def recommend_tickers(number):
    """
    This function select n random tickers from the database to provide
    some tickers to the clients.
    """

    try:
        if number > 20:
            raise ValueError("Requested to many number of tickers for recommendation.")

        with open(Path(__file__).parent / US_STOCK_FILE_NAME, "r") as file:
            all_tickers = json.load(file)

        ranks = random.sample(range(1, 101), number)
        tickers = []

        for rank in ranks:
            tickers.append(all_tickers[str(rank)]["ticker"])

        return tickers

    except Exception:
        return [
            "NVDA",
            "AAPL",
            "UBER",
            "NOW",
            "PG",
            "V",
            "AMZN",
            "AMAT",
            "CAT",
            "AVGO",
            "XOM",
        ]
