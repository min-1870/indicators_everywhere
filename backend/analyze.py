from fetch import fetch_data
from indicators import calculate_bb, calculate_gdc, calculate_macd, calculate_obv, calculate_rsi

def analyze_stock(symbol, window):

    def summarize_signal(dates, signal):

        buy = 0
        sell = 0
        neutral = 0

        history = []

        for i in range(len(signal)):
            date = dates[i].strftime('%Y-%m-%d')
            if signal['buy'].iloc[i]:
                history.append(f'Buy - {date}')
                buy += 1

            elif signal['sell'].iloc[i]:
                history.append(f'Sell - {date}')
                sell += 1
            
            else:
                history.append(f'Neutral - {date}')
                neutral += 1

        if buy > 0 and sell == 0:
            summary = 'Buy'
        elif sell > 0 and buy == 0:
            summary = 'Sell'
        else:
            summary = 'Neutral'

        count = buy + sell

        return {
            'indicator': signal['indicator'],
            'summary': summary,
            'count': count,
            'history': history
        }
    
    def summarize_overall_signal(summarized_signals):
        
        result = {
            'buy':0,
            'sell':0,
            'neutral':0,
            'signal':None,
        }

        for summarized_signal in summarized_signals:
            if summarized_signal['summary'] == 'Buy':
                result['buy'] += 1
            elif summarized_signal['summary'] == 'Sell':
                result['sell'] += 1
            elif summarized_signal['summary'] == 'Neutral':
                result['neutral'] += 1

        total = (
            result['buy'] +
            result['sell'] +
            result['neutral']
        )

        if result['buy'] > result['sell']:
            if result['buy'] > total / 2:
                result['signal'] = 'Strong Buy'

            else:
                result['signal'] = 'Buy'

        elif result['sell'] > result['buy']:
            if result['sell'] > total / 2:
                result['signal'] = 'Strong Sell'

            else:
                result['signal'] = 'Sell'

        else:
            result['signal'] = 'Stay'
            
        return result

    # Fetch history prices
    try:
        stock_data = fetch_data(symbol, 300)
    except:
        raise ValueError("Failed to fetch finance history from Yahoo.")
    
    if len(stock_data) < 200:
        raise ValueError("The history is not long enough.")
            
    # Calculate Indicators
    calculated_signals = [
        calculate_bb(stock_data, window),
        calculate_gdc(stock_data, window),
        calculate_macd(stock_data, window),
        calculate_obv(stock_data, window),
        calculate_rsi(stock_data, window)
    ]
     
    # Summarize the calculated signals
    signals = []
    for signal in calculated_signals:
        dates = stock_data.tail(window).index.tolist()
        signals.append(summarize_signal(dates, signal))

    # Summarize overall signals
    summary = summarize_overall_signal(signals)
            
    return {
        'summary': summary,
        'signals': signals
    }
    
# print(analyze_stock('NVDA', 5))
