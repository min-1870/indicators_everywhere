import pandas_ta as ta
from src.app.helpers import plot_graph, plot_two_graphs
from src.app.constants import INDICATORS_DETAIL


def calculate_obv(stock_symbol, stock_data, window=14):
    """
    On-Balance Volume (OBV)
    Buy: OBV is trending up while price is flat or rising
    Sell: OBV is trending down while price is flat or falling
    """

    # Calculate indicator values
    target_stock_data = stock_data.tail(window * 2).copy()
    target_stock_data["OBV"] = ta.obv(target_stock_data["Close"], target_stock_data["Volume"])
    target_stock_data["OBV_trend"] = target_stock_data["OBV"].diff(window)
    target_stock_data["Price_trend"] = target_stock_data["Close"].diff(window)
    target_stock_data = target_stock_data.tail(window)

    # OBV is trending up while price is flat or rising
    buy_signal = (
        (target_stock_data["OBV_trend"] > 0) & (target_stock_data["Price_trend"] >= 0)
    ).tolist()

    # OBV is trending down while price is flat or falling
    sell_signal = (
        (target_stock_data["OBV_trend"] < 0) & (target_stock_data["Price_trend"] <= 0)
    ).tolist()

    column1 = {"column": "OBV", "label": "OBV", "color": "red", "linestyle": "-"}
    column2 = {"column": "Close", "label": "Price", "color": "blue", "linestyle": "-"}

    graph_url = plot_two_graphs(
        stock_symbol, "OBV", window, target_stock_data, column1, column2
    )

    return {
        "name": INDICATORS_DETAIL["ovb"]["name"],
        "detail": INDICATORS_DETAIL["ovb"]["detail"],
        "buy": buy_signal,
        "sell": sell_signal,
        "graph_url": graph_url,
    }


def calculate_rsi(stock_symbol, stock_data, window=14):
    """
    Relative Strength Index
    Buy: RSI < 30 (oversold condition)
    Sell: RSI > 70 (overbought condition)
    """

    # Calculate indicator values
    target_stock_data = stock_data.tail(window * 2).copy()
    delta = target_stock_data["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    target_stock_data["RSI"] = 100 - (100 / (1 + rs))
    target_stock_data = target_stock_data.tail(window)

    # Track signals
    buy_signal = (target_stock_data["RSI"] < 30).tolist()

    sell_signal = (target_stock_data["RSI"] > 70).tolist()

    graph_url = plot_graph(
        stock_symbol,
        "RSI",
        window,
        target_stock_data,
        "RSI",
        [{"column": "RSI", "linestyle": "-", "color": "red", "label": "RSI"}],
        [
            {"y": 30, "linestyle": "--", "color": "yellow", "label": "Low RSI"},
            {"y": 70, "linestyle": "--", "color": "blue", "label": "High RSI"},
        ],
    )

    return {
        "name": INDICATORS_DETAIL["rsi"]["name"],
        "detail": INDICATORS_DETAIL["rsi"]["detail"],
        "buy": buy_signal,
        "sell": sell_signal,
        "graph_url": graph_url,
    }


def calculate_macd(stock_symbol, stock_data, window=14):
    """
    Moving Average Convergence Divergence
    Buy: MACD line crosses above the signal line
    Sell: MACD line crosses below the signal line
    """

    # Calculate indicator values
    target_stock_data = stock_data.tail(window * 7).copy()
    exp1 = target_stock_data["Close"].ewm(span=12, adjust=False).mean()
    exp2 = target_stock_data["Close"].ewm(span=26, adjust=False).mean()
    target_stock_data["MACD"] = exp1 - exp2
    target_stock_data["Signal_Line"] = target_stock_data["MACD"].ewm(span=9, adjust=False).mean()
    target_stock_data = target_stock_data.tail(window)

    # Track signals
    buy_signal = (
        (target_stock_data["MACD"].shift(1) < target_stock_data["Signal_Line"].shift(1))
        & (target_stock_data["MACD"] > target_stock_data["Signal_Line"])
    ).tolist()

    sell_signal = (
        (target_stock_data["MACD"].shift(1) > target_stock_data["Signal_Line"].shift(1))
        & (target_stock_data["MACD"] < target_stock_data["Signal_Line"])
    ).tolist()

    graph_url = plot_graph(
        stock_symbol,
        "MACD",
        window,
        target_stock_data,
        "MACD",
        [
            {"column": "MACD", "linestyle": "-", "color": "red", "label": "MACD"},
            {
                "column": "Signal_Line",
                "linestyle": "--",
                "color": "green",
                "label": "Signal Line",
            },
        ],
    )

    return {
        "name": INDICATORS_DETAIL["macd"]["name"],
        "detail": INDICATORS_DETAIL["macd"]["detail"],
        "buy": buy_signal,
        "sell": sell_signal,
        "graph_url": graph_url,
    }


def calculate_bb(stock_symbol, stock_data, window=14):
    """
    Bollinger Bands
    Buy: Price touches or goes below the lower band
    Sell: Price touches or goes above the upper band
    """

    # Calculate indicator values
    target_stock_data = stock_data.tail(window * 3).copy()
    target_stock_data["MA20"] = target_stock_data["Close"].rolling(window=20).mean()
    target_stock_data["20d_std"] = target_stock_data["Close"].rolling(window=20).std()
    target_stock_data["Upper_BB"] = target_stock_data["MA20"] + (target_stock_data["20d_std"] * 2)
    target_stock_data["Lower_BB"] = target_stock_data["MA20"] - (target_stock_data["20d_std"] * 2)
    target_stock_data = target_stock_data.tail(window)

    # Track signals
    buy_signal = (target_stock_data["Lower_BB"] >= target_stock_data["Close"]).tolist()

    sell_signal = (target_stock_data["Upper_BB"] <= target_stock_data["Close"]).tolist()

    graph_url = plot_graph(
        stock_symbol,
        "BB",
        window,
        target_stock_data,
        "Price",
        [
            {"column": "Close", "linestyle": "-", "color": "red", "label": "Price"},
            {
                "column": "Upper_BB",
                "linestyle": "--",
                "color": "green",
                "label": "Upper band",
            },
            {
                "column": "Lower_BB",
                "linestyle": "--",
                "color": "blue",
                "label": "Lower band",
            },
        ],
    )

    return {
        "name": INDICATORS_DETAIL["bb"]["name"],
        "detail": INDICATORS_DETAIL["bb"]["detail"],
        "buy": buy_signal,
        "sell": sell_signal,
        "graph_url": graph_url,
    }


def calculate_gdc(stock_symbol, stock_data, window=14):
    """
    Golden/Death Cross
    Buy: 50-day MA crosses above 200-day MA
    Sell: 50-day MA crosses below 200-day MA
    """

    # Calculate indicator values
    target_stock_data = stock_data.copy()
    target_stock_data["SMA50"] = target_stock_data["Close"].rolling(window=140).mean()
    target_stock_data["SMA200"] = target_stock_data["Close"].rolling(window=200).mean()
    target_stock_data = target_stock_data.tail(window)

    # Track signals
    buy_signal = (
        (target_stock_data["SMA50"].shift(1) < target_stock_data["SMA200"].shift(1))
        & (target_stock_data["SMA50"] > target_stock_data["SMA200"])
    ).tolist()

    sell_signal = (
        (target_stock_data["SMA50"].shift(1) > target_stock_data["SMA200"].shift(1))
        & (target_stock_data["SMA50"] < target_stock_data["SMA200"])
    ).tolist()

    graph_url = plot_graph(
        stock_symbol,
        "GDC",
        window,
        target_stock_data,
        "Price",
        [
            {"column": "Close", "linestyle": "-", "color": "red", "label": "Price"},
            {"column": "SMA50", "linestyle": "-", "color": "green", "label": "SMA50"},
            {"column": "SMA200", "linestyle": "-", "color": "blue", "label": "SMA200"},
        ],
    )

    return {
        "name": INDICATORS_DETAIL["gdc"]["name"],
        "detail": INDICATORS_DETAIL["gdc"]["detail"],
        "buy": buy_signal,
        "sell": sell_signal,
        "graph_url": graph_url,
    }


def calculate_so(stock_symbol, stock_data, window=14):
    """
    Stochastic Oscillator
    Buy: When %K line crosses above %D line and both lines are below 20
    Sell: When %K line crosses below %D line and both lines are above 80
    """

    # Calculate indicator values
    target_stock_data = stock_data.tail(window * 3).copy()
    low_min = target_stock_data["Low"].rolling(window=window).min()
    high_max = target_stock_data["High"].rolling(window=window).max()
    target_stock_data["%K_raw"] = 100 * (target_stock_data["Close"] - low_min) / (high_max - low_min)
    target_stock_data["%K"] = target_stock_data["%K_raw"].rolling(window=3).mean()
    target_stock_data["%D"] = target_stock_data["%K"].rolling(window=3).mean()
    target_stock_data = target_stock_data.tail(window)

    # Track signals
    buy_signal = (
        (target_stock_data["%K"].shift(1) < target_stock_data["%D"].shift(1))
        & (target_stock_data["%K"] > target_stock_data["%D"])
        & (target_stock_data["%K"] < 20)
        & (target_stock_data["%D"] < 20)
    ).tolist()

    sell_signal = (
        (target_stock_data["%K"].shift(1) > target_stock_data["%D"].shift(1))
        & (target_stock_data["%K"] < target_stock_data["%D"])
        & (target_stock_data["%K"] > 80)
        & (target_stock_data["%D"] > 80)
    ).tolist()

    graph_url = plot_graph(
        stock_symbol,
        "SO",
        window,
        target_stock_data,
        "Stochastic Oscillator",
        [
            {"column": "%K", "linestyle": "-", "color": "blue", "label": "%K"},
            {"column": "%D", "linestyle": "-", "color": "red", "label": "%D"},
        ],
    )

    return {
        "name": INDICATORS_DETAIL["so"]["name"],
        "detail": INDICATORS_DETAIL["so"]["detail"],
        "buy": buy_signal,
        "sell": sell_signal,
        "graph_url": graph_url,
    }


def calculate_atr(stock_symbol, stock_data, window=14):
    """
    Average True Range
    Buy: ATR increases significantly, indicating potential for high volatility
    Sell: ATR decreases, indicating low volatility
    """

    # Calculate indicator values
    target_stock_data = stock_data.tail(window * 2 - 1).copy()
    target_stock_data["ATR"] = ta.atr(
        target_stock_data["High"], target_stock_data["Low"], target_stock_data["Close"], window=window
    )
    target_stock_data["ATR_trend"] = target_stock_data["ATR"].diff()
    target_stock_data = target_stock_data.tail(window)

    # Track signals
    buy_signal = (
        target_stock_data["ATR_trend"] > 0.1 * target_stock_data["ATR"].shift(1)
    ).tolist()
    sell_signal = (
        target_stock_data["ATR_trend"] < -0.1 * target_stock_data["ATR"].shift(1)
    ).tolist()

    graph_url = plot_graph(
        stock_symbol,
        "ATR",
        window,
        target_stock_data,
        "ATR",
        [{"column": "ATR", "linestyle": "-", "color": "red", "label": "ATR"}],
    )

    return {
        "name": INDICATORS_DETAIL["atr"]["name"],
        "detail": INDICATORS_DETAIL["atr"]["detail"],
        "buy": buy_signal,
        "sell": sell_signal,
        "graph_url": graph_url,
    }


def calculate_frl(stock_symbol, stock_data, window=14):
    """
    Fibonacci Retracement Levels
    Buy: Price retraces to a key Fibonacci level (23.6%, 38.2%, 50%, or 61.8%)
    and bounces back.
    Sell: Price fails to hold a retracement level and moves lower.
    """

    # Calculate the highest high and the lowest low in the window
    highest_high = stock_data["High"].tail(window).max()
    lowest_low = stock_data["Low"].tail(window).min()

    # Calculate Fibonacci levels
    diff = highest_high - lowest_low
    fib_levels = {
        "Level_0": highest_high,
        "Level_236": highest_high - 0.236 * diff,  # 23.6% Fibonacci level
        "Level_382": highest_high - 0.382 * diff,  # 38.2% Fibonacci level
        "Level_50": highest_high - 0.5 * diff,  # 50% Fibonacci level
        "Level_618": highest_high - 0.618 * diff,  # 61.8% Fibonacci level
        "Level_100": lowest_low,
    }

    # Get the most recent price data for the window
    target_stock_data = stock_data.tail(window)

    # Initialize signals
    buy_signal = []
    sell_signal = []

    # Loop through the data to check for signals
    for i in range(len(target_stock_data)):

        current_price = target_stock_data["Close"].iloc[i]
        previous_price = target_stock_data["Close"].iloc[i - 1]
        # Buy signal: price bounces from a key Fibonacci level
        if (
            current_price > fib_levels["Level_236"]
            and previous_price < fib_levels["Level_236"]
        ):
            buy_signal.append(True)
        elif (
            current_price > fib_levels["Level_382"]
            and previous_price < fib_levels["Level_382"]
        ):
            buy_signal.append(True)
        elif (
            current_price > fib_levels["Level_50"]
            and previous_price < fib_levels["Level_50"]
        ):
            buy_signal.append(True)
        elif (
            current_price > fib_levels["Level_618"]
            and previous_price < fib_levels["Level_618"]
        ):
            buy_signal.append(True)
        else:
            buy_signal.append(False)

        # Sell signal: price fails to hold a Fibonacci level and moves lower
        if (
            current_price > fib_levels["Level_236"]
            and previous_price < fib_levels["Level_236"]
        ):
            sell_signal.append(True)
        elif (
            current_price > fib_levels["Level_382"]
            and previous_price < fib_levels["Level_382"]
        ):
            sell_signal.append(True)
        elif (
            current_price < fib_levels["Level_50"]
            and previous_price > fib_levels["Level_50"]
        ):
            sell_signal.append(True)
        elif (
            current_price < fib_levels["Level_618"]
            and previous_price > fib_levels["Level_618"]
        ):
            sell_signal.append(True)
        else:
            sell_signal.append(False)

    graph_url = plot_graph(
        stock_symbol,
        "FIB",
        window,
        target_stock_data,
        "Price",
        [{"column": "Close", "linestyle": "-", "color": "red", "label": "Price"}],
        [
            {
                "y": fib_levels["Level_0"],
                "linestyle": "--",
                "color": "yellow",
                "label": "Level 0",
            },
            {
                "y": fib_levels["Level_236"],
                "linestyle": "--",
                "color": "orange",
                "label": "Level 236",
            },
            {
                "y": fib_levels["Level_382"],
                "linestyle": "--",
                "color": "green",
                "label": "Level 382",
            },
            {
                "y": fib_levels["Level_50"],
                "linestyle": "--",
                "color": "blue",
                "label": "Level 50",
            },
            {
                "y": fib_levels["Level_618"],
                "linestyle": "--",
                "color": "purple",
                "label": "Level 618",
            },
            {
                "y": fib_levels["Level_100"],
                "linestyle": "--",
                "color": "black",
                "label": "Level 100",
            },
        ],
    )

    return {
        "name": INDICATORS_DETAIL["frl"]["name"],
        "detail": INDICATORS_DETAIL["frl"]["detail"],
        "buy": buy_signal,
        "sell": sell_signal,
        "graph_url": graph_url,
    }


def calculate_sar(stock_symbol, stock_data, window=14):
    """
    Parabolic SAR
    Buy: When the current closing price is greater than the Parabolic SAR and the previous closing price was below the SAR.
    Sell: When the current closing price is less than the Parabolic SAR and the previous closing price was above the SAR.
    """

    indicator_short_name = 'SAR'

    # Calculate indicator value
    target_stock_data = stock_data.tail(window).copy()
    psar = ta.psar(target_stock_data['High'], target_stock_data['Low']) 
    target_stock_data[indicator_short_name] = psar['PSARl_0.02_0.2']   

    # Track signals
    buy_signal = ((target_stock_data['Close'] > target_stock_data[indicator_short_name]) & (target_stock_data['Close'].shift(1) < target_stock_data[indicator_short_name].shift(1))).tolist()
    sell_signal = ((target_stock_data['Close'] < target_stock_data[indicator_short_name]) & (target_stock_data['Close'].shift(1) > target_stock_data[indicator_short_name].shift(1))).tolist()

    graph_url = plot_graph(
        stock_symbol,
        indicator_short_name,
        window,
        target_stock_data,
        indicator_short_name,
        [{"column": "Close", "linestyle": "-", "color": "red", "label": "Price"},
         {"column": indicator_short_name, "linestyle": "--", "color": "blue", "label": indicator_short_name}],
    )

    return {
        "name": INDICATORS_DETAIL[indicator_short_name]["name"],
        "detail": INDICATORS_DETAIL[indicator_short_name]["detail"],
        "buy": buy_signal,
        "sell": sell_signal,
        "graph_url": graph_url,
    }


def calculate_wil(stock_symbol, stock_data, window=14):
    """
    Williams %R
    Buy: Williams %R crosses above -80 (oversold).
    Sell: Williams %R crosses below -20 (overbought).
    """

    indicator_short_name = 'WIL'

    # Calculate indicator value
    target_stock_data = stock_data.tail(window * 2 - 1).copy()
    target_stock_data[indicator_short_name] = ta.willr(target_stock_data['High'], target_stock_data['Low'], target_stock_data['Close'], length=window)
    target_stock_data = target_stock_data.tail(window)

    # Track signals    
    buy_signal = ((target_stock_data[indicator_short_name] > -80) & (target_stock_data[indicator_short_name].shift(1) <= -80)).tolist()
    sell_signal = ((target_stock_data[indicator_short_name] < -20) & (target_stock_data[indicator_short_name].shift(1) >= -20)).tolist()

    graph_url = plot_graph(
        stock_symbol,
        indicator_short_name,
        window,
        target_stock_data,
        indicator_short_name,
        [{"column": indicator_short_name, "linestyle": "-", "color": "red", "label": indicator_short_name}],
        [{"y": -80, "linestyle": "--", "color": "blue", "label": 'oversold'},
        {"y": -20, "linestyle": "--", "color": "green", "label": 'overbought'}]
    )
    
    return {
        "name": INDICATORS_DETAIL[indicator_short_name]["name"],
        "detail": INDICATORS_DETAIL[indicator_short_name]["detail"],
        "buy": buy_signal,
        "sell": sell_signal,
        "graph_url": graph_url,
    }


def calculate_dmi(stock_symbol, stock_data, window=14):
    """
    Directional Movement Index
    Buy: When +DI crosses above -DI.
    Sell: When -DI crosses above +DI.
    """

    indicator_short_name = 'DMI'

    # Calculate indicator value
    target_stock_data = stock_data.tail(window * 2 - 1).copy()
    dmi = ta.dm(target_stock_data['High'], target_stock_data['Low'], length=window)
    target_stock_data = target_stock_data.join(dmi)
    target_stock_data = target_stock_data.tail(window)

    # Track signals    
    buy_signal = ((target_stock_data['DMP_14'] > target_stock_data['DMN_14']) & (target_stock_data['DMP_14'].shift(1) <= target_stock_data['DMN_14'].shift(1))).tolist()
    sell_signal = ((target_stock_data['DMN_14'] > target_stock_data['DMP_14']) & (target_stock_data['DMN_14'].shift(1) <= target_stock_data['DMP_14'].shift(1))).tolist()

    graph_url = plot_graph(
        stock_symbol,
        indicator_short_name,
        window,
        target_stock_data,
        indicator_short_name,
        [{"column": 'DMP_14', "linestyle": "-", "color": "red", "label": 'DMP 14'},
         {"column": 'DMN_14', "linestyle": "-", "color": "blue", "label": 'DMN 14'}],
    )
    
    return {
        "name": INDICATORS_DETAIL[indicator_short_name]["name"],
        "detail": INDICATORS_DETAIL[indicator_short_name]["detail"],
        "buy": buy_signal,
        "sell": sell_signal,
        "graph_url": graph_url,
    }


def calculate_cmf(stock_symbol, stock_data, window=14):
    """
    Chaikin Money Flow 
    Buy: When CMF crosses above zero, indicating accumulation.
    Sell: When CMF crosses below zero, indicating distribution.
    """

    indicator_short_name = 'CMF'

    # Calculate indicator value
    target_stock_data = stock_data.tail(window*2-1).copy()
    target_stock_data[indicator_short_name] = ta.cmf(high=target_stock_data['High'], low=target_stock_data['Low'], close=target_stock_data['Close'], volume=target_stock_data['Volume'], length=window)
    target_stock_data = target_stock_data.tail(window)
    
    # Track signals   
    buy_signal = ((target_stock_data[indicator_short_name] > 0) & (target_stock_data[indicator_short_name].shift(1) <= 0)).tolist()
    sell_signal = ((target_stock_data[indicator_short_name] < 0) & (target_stock_data[indicator_short_name].shift(1) >= 0)).tolist()
    
    graph_url = plot_graph(
        stock_symbol,
        indicator_short_name,
        window,
        target_stock_data,
        indicator_short_name,
        [{"column": indicator_short_name, "linestyle": "-", "color": "red", "label": indicator_short_name}],
        [{"y": 0, "linestyle": "--", "color": "blue", "label": 'Zero'}],
    )
    
    return {
        "name": INDICATORS_DETAIL[indicator_short_name]["name"],
        "detail": INDICATORS_DETAIL[indicator_short_name]["detail"],
        "buy": buy_signal,
        "sell": sell_signal,
        "graph_url": graph_url,
    }
