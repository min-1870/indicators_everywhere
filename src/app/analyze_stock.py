from src.app.api import fetch_data
from src.app import calculators


def analyze_stock(stock_symbol, window=14):
    """
    This function calculate the individual indicators of the tickers
    to provide indicators value and graphs of the tickers to the clients.
    """

    def summarize_signal(dates, signal):

        latest_signal = "Neutral"
        history = []

        for i in range(len(signal["buy"])):
            date = dates[i].strftime("%Y-%m-%d")
            if signal["buy"][i]:
                history.append(f"Buy - {date}")
                latest_signal = "Buy"

            elif signal["sell"][i]:
                history.append(f"Sell - {date}")
                latest_signal = "Sell"

            else:
                history.append(f"Neutral - {date}")

        return {
            "name": signal["name"],
            "detail": signal["detail"],
            "summary": latest_signal,
            "graph_url": signal["graph_url"],
            "history": history,
        }

    def summarize_overall_signal(summarized_signals):

        result = {
            "buy": 0,
            "sell": 0,
            "neutral": 0,
            "signal": None,
        }

        for summarized_signal in summarized_signals:
            if summarized_signal["summary"] == "Buy":
                result["buy"] += 1
            elif summarized_signal["summary"] == "Sell":
                result["sell"] += 1
            elif summarized_signal["summary"] == "Neutral":
                result["neutral"] += 1

        total = result["buy"] + result["sell"] + result["neutral"]

        if result["buy"] > result["sell"]:
            if result["buy"] > total / 2:
                result["signal"] = "Strong Buy"

            else:
                result["signal"] = "Buy"

        elif result["sell"] > result["buy"]:
            if result["sell"] > total / 2:
                result["signal"] = "Strong Sell"

            else:
                result["signal"] = "Sell"

        else:
            result["signal"] = "Stay"

        return result

    # Fetch history prices
    stock_data = fetch_data(stock_symbol, 300)

    if len(stock_data) < 200:
        raise ValueError("Failed to fetch the enough length of the finance history.")

    # Calculate Indicators
    calculated_signals = [
        calculators.calculate_bb(stock_symbol, stock_data, window),
        calculators.calculate_gdc(stock_symbol, stock_data, window),
        calculators.calculate_macd(stock_symbol, stock_data, window),
        calculators.calculate_obv(stock_symbol, stock_data, window),
        calculators.calculate_rsi(stock_symbol, stock_data, window),
        calculators.calculate_so(stock_symbol, stock_data, window),
        calculators.calculate_atr(stock_symbol, stock_data, window),
        calculators.calculate_frl(stock_symbol, stock_data, window),
        calculators.calculate_sar(stock_symbol, stock_data, window),
        calculators.calculate_wil(stock_symbol, stock_data, window),
        calculators.calculate_dmi(stock_symbol, stock_data, window),
        calculators.calculate_cmf(stock_symbol, stock_data, window),
    ]

    # Summarize the calculated signals
    indicators = []
    for signal in calculated_signals:
        dates = stock_data.tail(window).index.tolist()
        indicators.append(summarize_signal(dates, signal))

    # Summarize overall signals
    summary = summarize_overall_signal(indicators)

    return {"summary": summary, "indicators": indicators}
