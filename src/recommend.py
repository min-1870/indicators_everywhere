from constants import US_STOCK_FILE_NAME
from pathlib import Path
import json
import random

def recommend_tickers(number):
    with open(Path(__file__).parent / US_STOCK_FILE_NAME, 'r') as file:
        all_tickers = json.load(file)

    ranks = random.sample(range(1, 101), number)
    tickers = []

    for rank in ranks:
        tickers.append(all_tickers[str(rank)]['ticker'])
    
    return tickers