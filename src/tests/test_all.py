from src.app import calculators
from src.app.api import fetch_data
from src.app.recommend_tickers import recommend_tickers
from src.app.analyze_stock import analyze_stock

TICKER = "AAPL"
WINDOW = 14


def test_calculators_output_structure():
    stock_data = fetch_data(TICKER, 300)

    results = [
        calculators.calculate_obv(TICKER, stock_data, WINDOW),
        calculators.calculate_rsi(TICKER, stock_data, WINDOW),
        calculators.calculate_macd(TICKER, stock_data, WINDOW),
        calculators.calculate_bb(TICKER, stock_data, WINDOW),
        calculators.calculate_gdc(TICKER, stock_data, WINDOW),
        calculators.calculate_so(TICKER, stock_data, WINDOW),
        calculators.calculate_atr(TICKER, stock_data, WINDOW),
        calculators.calculate_frl(TICKER, stock_data, WINDOW),
    ]

    for result in results:

        assert type(result["buy"]) is list
        assert len(result["buy"]) == WINDOW
        for signal in result["buy"]:
            assert type(signal) is bool

        assert type(result["sell"]) is list
        assert len(result["sell"]) == WINDOW
        for signal in result["sell"]:
            assert type(signal) is bool


def test_analyze_stock_output_structure():
    result = analyze_stock(TICKER, WINDOW)

    assert list(result.keys()) == ["summary", "indicators"]
    assert list(result["summary"].keys()) == ["buy", "sell", "neutral", "signal"]
    assert list(result["indicators"][0].keys()) == [
        "name",
        "detail",
        "summary",
        "graph_url",
        "history",
    ]
    assert type(result["indicators"][0]["history"]) is list
    assert len(result["indicators"][0]["history"]) == WINDOW


def test_recommend_tickers():

    tickers = recommend_tickers(10)

    assert type(tickers) is list
    assert len(tickers) == 10
