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
    "SAR": {
        "name": "Parabolic SAR",
        "detail": """The Parabolic SAR (Stop and Reverse) is a trend-following
         indicator used to identify potential trend reversals and determine
         buy or sell signals. It is plotted as a series of dots above or below
         the price chart. When the price is in an uptrend, the SAR dots are
         placed below the price, and when the price is in a downtrend, the SAR
         dots are placed above the price. A buy signal is generated when the
         price crosses above the SAR, indicating a potential trend reversal to
         the upside. Conversely, a sell signal is generated when the price
         crosses below the SAR, signaling a potential trend reversal to the
         downside.""",
    },
    "WIL": {
        "name": "Williams %R",
        "detail": """The Williams %R is a momentum oscillator that measures the level
         of the close relative to the high-low range over a specified period,
         typically 14 days. It fluctuates between 0 and -100, with readings above -20
         considered overbought and below -80 considered oversold. The indicator helps
         identify potential trend reversals and market entry or exit points. A buy
         signal is generated when the %R moves from oversold territory (below -80)
         back above -80, indicating a potential upward trend reversal. Conversely, a
         sell signal occurs when the %R moves from overbought territory (above -20)
         back below -20, suggesting a potential downward trend reversal. However,
         traders often use additional confirmation signals, as overbought or oversold
         conditions can persist in strong trends.""",
    },
    "DMI": {
        "name": "Directional Movement Index",
        "detail": """The Directional Movement Index (DMI) is a technical analysis
         indicator developed by J. Welles Wilder to assess the strength and
         direction of a price trend. It consists of three components: the
         Positive Directional Indicator (+DI), the Negative Directional Indicator
         (-DI), and the Average Directional Index (ADX). The +DI measures upward
         price movement, while the -DI measures downward price movement. When +DI
         is above -DI, it indicates bullish pressure, suggesting a potential buy
         signal. Conversely, when -DI is above +DI, it indicates bearish pressure,
         signaling a potential sell signal. The ADX quantifies the strength of the
         trend, with values above 25 typically indicating a strong trend.
         Crossovers between +DI and -DI are often used as trade signals, providing
         traders with insights into potential market movements.""",
    },
    "CMF": {
        "name": "Chaikin Money Flow",
        "detail": """The Chaikin Money Flow (CMF) is a momentum indicator developed by
         Marc Chaikin that measures the volume of money flowing into and out of an
         asset over a specified period, typically 21 days. The CMF is based on the
         principle that when the closing price is closer to the high of the period, it
         indicates accumulation (buying pressure), while a closing price closer to the
         low suggests distribution (selling pressure). The CMF oscillates between -1
         and +1, with positive values indicating strong buying pressure and negative
         values indicating selling pressure. A buy signal is generated when the CMF
         crosses above zero, confirming an uptrend, while a sell signal occurs when it
         crosses below zero, suggesting a potential downtrend. Additionally,
         divergences between price action and CMF can signal potential trend
         reversals, making it a valuable tool for traders to assess market strength
         and make informed trading decisions.""",
    },
}
