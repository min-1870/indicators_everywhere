S3_BUCKET_NAME = "indicators-everywhere"
S3_GRAPHS_PATH = "graphs/"
LOCAL_GRAPHS_PATH = "graphs"
US_STOCK_FILE_NAME = "us_stock.json"
DEBUG = False
TICKERS_RECOMMEND_NUMBER = 20
PLOT_GRID = True
PLOT_BOX = True
S3_URL_TO_GRAPHS = (
    f"https://{S3_BUCKET_NAME}.s3.ap-southeast-2.amazonaws.com/{S3_GRAPHS_PATH}"
)
INDICATORS_DETAIL = {
    "ovb": {
        "name": "On-Balance Volume",
        "detail": """On-Balance Volume is a technical analysis indicator that measures
         buying and selling pressure based on volume. It works by adding the day's
         volume to a cumulative total when the price closes higher, and subtracting
         the day's volume when the price closes lower. The idea behind OBV is that
         changes in volume often precede price movements, providing insights into
         potential trends. Traders use OBV to confirm trends or identify divergences
         between volume and price action, which can signal potential reversals.""",
    },
    "rsi": {
        "name": "Relative Strength Index",
        "detail": """The Relative Strength Index is a momentum oscillator that
         measures the speed and change of price movements. It ranges from 0 to
         100 and is typically used to identify overbought or oversold
         conditions in a market. An RSI above 70 is considered overbought,
         suggesting a potential reversal or correction, while an RSI below 30
         is considered oversold, indicating a potential buying opportunity.
         RSI helps traders gauge the strength of a price trend and identify
         potential reversals.""",
    },
    "macd": {
        "name": "Moving Average Convergence Divergence",
        "detail": """The Moving Average Convergence Divergence is a trend-following
         momentum indicator that shows the relationship between two moving averages
         of a security’s price. It is calculated by subtracting the 26-period
         exponential moving average (EMA) from the 12-period EMA. A 9-period EMA of
         the MACD line, called the 'signal line', is then plotted on top of the MACD
         line. MACD is used to identify potential buy and sell signals through
         crossovers, divergences, and overbought/oversold conditions.""",
    },
    "bb": {
        "name": "Bollinger Bands",
        "detail": """Bollinger Bands are a volatility indicator that consists of
         three lines: a simple moving average (SMA) in the middle, and two outer
         bands that are a specified number of standard deviations away from the
         SMA. The outer bands expand and contract based on market volatility,
         with wider bands indicating higher volatility and narrower bands
         indicating lower volatility. Bollinger Bands help traders identify
         overbought and oversold conditions, as well as potential breakout
         opportunities.""",
    },
    "gdc": {
        "name": "Golden/Death Cross",
        "detail": """The Golden Cross and Death Cross are popular technical indicators
         that use moving averages to signal potential market trends. A Golden Cross
         occurs when a short-term moving average (typically the 50-day SMA) crosses
         above a long-term moving average (typically the 200-day SMA), signaling a
         potential bullish trend. A Death Cross occurs when the short-term moving
         average crosses below the long-term moving average, signaling a potential
         bearish trend. These crosses are often used to identify long-term trend
         changes.""",
    },
    "so": {
        "name": "Stochastic Oscillator",
        "detail": """The Stochastic Oscillator is a momentum indicator that compares a
         security's closing price to its price range over a specific period of time.
         It consists of two lines: %K and %D. The %K line represents the current
         closing price relative to the price range, while the %D line is a moving
         average of the %K line. The Stochastic Oscillator ranges from 0 to 100 and is
         typically used to identify overbought (above 80) and oversold (below 20)
         conditions, as well as potential price reversals when the lines cross.""",
    },
    "atr": {
        "name": "Average True Range",
        "detail": """The Average True Range (ATR) is a volatility indicator that
         measures market volatility by decomposing the entire range of an asset
         price for that period. ATR does not indicate price direction, but rather
         the degree of price movement or volatility. A higher ATR value indicates
         higher volatility, while a lower ATR value indicates lower volatility.
         Traders use ATR to assess the potential risk or reward of entering or
         exiting a trade and to set stop-loss levels that adjust to volatility.""",
    },
    "frl": {
        "name": "Fibonacci Retracement Levels",
        "detail": """Fibonacci Retracement Levels are a popular technical analysis tool
         used to identify potential support and resistance levels based on the
         Fibonacci sequence. The key retracement levels (23.6%, 38.2%, 50%, 61.8%, and
         100%) are derived from the Fibonacci sequence and are used to predict
         potential price reversals during a pullback in a trending market. Traders use
         these levels to identify buying and selling opportunities when the price
         retraces to these levels and shows signs of reversal or continuation of the
         trend.""",
    },
}
