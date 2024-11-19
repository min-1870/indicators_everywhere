import pandas_ta as ta
from helper_functions import plot_graph, plot_two_graphs

def calculate_obv(stock_symbol, stock_data, window=5):
    '''
    On-Balance Volume (OBV)
    Buy: OBV is trending up while price is flat or rising
    Sell: OBV is trending down while price is flat or falling
    '''


    # Calculate OBV only for the target data
    stock_data['OBV'] = ta.obv(stock_data['Close'], stock_data['Volume'])
    
    # Calculate OBV and price trends
    stock_data['OBV_trend'] = stock_data['OBV'].diff(window)
    stock_data['Price_trend'] = stock_data['Close'].diff(window)

    target_stock_data = stock_data.tail(window)

    # OBV is trending up while price is flat or rising
    buy_signal = (target_stock_data['OBV_trend'] > 0) & (target_stock_data['Price_trend'] >= 0)

    # OBV is trending down while price is flat or falling
    sell_signal = (target_stock_data['OBV_trend'] < 0) & (target_stock_data['Price_trend'] <= 0)

    plot_two_graphs(stock_symbol, 'OBV', window, target_stock_data, 'OBV', 'OBV', 'Close', 'Price')
    
    return {
        'indicator':'On-Balance Volume (OBV)',
        'buy':buy_signal,
        'sell':sell_signal
    }

def calculate_rsi(stock_symbol, stock_data, window=5):
    '''
    Relative Strength Index (RSI)
    Buy: RSI < 30 (oversold condition)
    Sell: RSI > 70 (overbought condition)
    '''

    delta = stock_data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    stock_data['RSI'] = 100 - (100 / (1 + rs))

    target_stock_data = stock_data.tail(window)

    # RSI < 30 (oversold condition)
    buy_signal = (target_stock_data['RSI'] < 30)

    # RSI > 70 (overbought condition)
    sell_signal = (target_stock_data['RSI'] > 70)

    plot_graph(stock_symbol, 'RSI', window, target_stock_data, 'RSI',[
        {
            'column':'RSI', 
            'linestyle':'-',
            'color':'red',
            'label':'RSI'
        }
    ])
    
    return {
        'indicator':'Relative Strength Index (RSI)',
        'buy':buy_signal,
        'sell':sell_signal
    }

def calculate_macd(stock_symbol, stock_data, window=5):
    '''
    Moving Average Convergence Divergence (MACD)
    Buy: MACD line crosses above the signal line
    Sell: MACD line crosses below the signal line
    '''

    exp1 = stock_data['Close'].ewm(span=12, adjust=False).mean()
    exp2 = stock_data['Close'].ewm(span=26, adjust=False).mean()
    stock_data['MACD'] = exp1 - exp2
    stock_data['Signal_Line'] = stock_data['MACD'].ewm(span=9, adjust=False).mean()

    target_stock_data = stock_data.tail(window)

    # MACD line crosses above the signal line
    buy_signal = (
        (target_stock_data['MACD'].shift(1) < target_stock_data['Signal_Line'].shift(1)) & 
        (target_stock_data['MACD'] > target_stock_data['Signal_Line']))

    # MACD line crosses below the signal line
    sell_signal = (
        (target_stock_data['MACD'].shift(1) > target_stock_data['Signal_Line'].shift(1)) & 
        (target_stock_data['MACD'] < target_stock_data['Signal_Line']))

    plot_graph(stock_symbol, 'MACD', window, target_stock_data, 'MACD',[
        {
            'column':'MACD', 
            'linestyle':'-',
            'color':'red',
            'label':'MACD'
        },
        {
            'column':'Signal_Line', 
            'linestyle':'--',
            'color':'green',
            'label':'Signal Line'
        }
    ])

    return {
        'indicator':'Moving Average Convergence Divergence (MACD)',
        'buy':buy_signal,
        'sell':sell_signal
    }

def calculate_bb(stock_symbol, stock_data, window=5):
    '''
    Bollinger Bands
    Buy: Price touches or goes below the lower band
    Sell: Price touches or goes above the upper band
    '''

    stock_data['MA20'] = stock_data['Close'].rolling(window=20).mean()
    stock_data['20d_std'] = stock_data['Close'].rolling(window=20).std()
    stock_data['Upper_BB'] = stock_data['MA20'] + (stock_data['20d_std'] * 2)
    stock_data['Lower_BB'] = stock_data['MA20'] - (stock_data['20d_std'] * 2)

    target_stock_data = stock_data.tail(window)

    # Price touches or goes below the lower band
    buy_signal = (target_stock_data['Lower_BB'] >= target_stock_data['Close'])

    # Price touches or goes above the upper band
    sell_signal = (target_stock_data['Upper_BB'] <= target_stock_data['Close'])

    plot_graph(stock_symbol, 'BB', window, target_stock_data, 'Price',[
        {
            'column':'Close', 
            'linestyle':'-',
            'color':'red',
            'label':'Price'
        },
        {
            'column':'Upper_BB', 
            'linestyle':'--',
            'color':'green',
            'label':'Upper band'
        },
        {
            'column':'Lower_BB', 
            'linestyle':'--',
            'color':'blue',
            'label':'Lower band'
        }
    ])

    return {
        'indicator':'Bollinger Bands',
        'buy':buy_signal,
        'sell':sell_signal
    }

def calculate_gdc(stock_symbol, stock_data, window=5):
    '''
    Golden/Death Cross
    Buy: 50-day MA crosses above 200-day MA
    Sell: 50-day MA crosses below 200-day MA
    '''

    stock_data['SMA50'] = stock_data['Close'].rolling(window=50).mean()
    stock_data['SMA200'] = stock_data['Close'].rolling(window=200).mean()

    target_stock_data = stock_data.tail(window)
    
    # 50-day MA crosses above 200-day MA
    buy_signal = ((target_stock_data['SMA50'].shift(1) < target_stock_data['SMA200'].shift(1)) &
                  (target_stock_data['SMA50'] > target_stock_data['SMA200']))

    # 50-day MA crosses below 200-day MA
    sell_signal = ((target_stock_data['SMA50'].shift(1) > target_stock_data['SMA200'].shift(1)) &
                   (target_stock_data['SMA50'] < target_stock_data['SMA200']))

    plot_graph(stock_symbol, 'GDC', window, target_stock_data, 'Price',[
        {
            'column':'Close', 
            'linestyle':'-',
            'color':'red',
            'label':'Price'
        },
        {
            'column':'SMA50', 
            'linestyle':'-',
            'color':'green',
            'label':'SMA50'
        },
        {
            'column':'SMA200', 
            'linestyle':'-',
            'color':'blue',
            'label':'SMA200'
        }
    ])

    return {
        'indicator':'Golden/Death Cross',
        
        # 50-day MA crosses above 200-day MA
        'buy':buy_signal,
        
        # 50-day MA crosses below 200-day MA
        'sell':sell_signal
    }

