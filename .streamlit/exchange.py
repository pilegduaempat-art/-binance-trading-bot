<details>
<summary><b>📄 exchange.py (Click to expand)</b></summary>
```python
"""
Exchange Module
Handles all exchange connections and data fetching
"""
import ccxt
import pandas as pd
import streamlit as st
@st.cache_resource
def get_exchange(api_key, api_secret, testnet=False):
"""Initialize and return Binance exchange connection"""
try:
options = {
'apiKey': api_key,
'secret': api_secret,
'enableRateLimit': True,
'options': {'defaultType': 'future'}
}
    if testnet:
        options['urls'] = {
            'api': {
                'public': 'https://testnet.binancefuture.com/fapi/v1',
                'private': 'https://testnet.binancefuture.com/fapi/v1'
            }
        }
    
    exchange = ccxt.binance(options)
    exchange.load_markets()
    return exchange

except Exception as e:
    st.error(f"❌ Exchange connection error: {e}")
    return None
@st.cache_data(ttl=60)
def fetch_ohlcv(api_key, api_secret, symbol, timeframe='5m', limit=500):
"""Fetch OHLCV candlestick data"""
exchange = get_exchange(api_key, api_secret)
if not exchange:
return None
try:
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(
        ohlcv, 
        columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
    )
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

except Exception as e:
    return None
def fetch_orderbook(exchange, symbol):
"""Fetch order book data"""
try:
return exchange.fetch_order_book(symbol, limit=20)
except:
return None
def fetch_funding_rate(exchange, symbol):
"""Fetch current funding rate"""
try:
return exchange.fetch_funding_rate(symbol)
except:
return None
def get_top_volume_pairs(exchange, num_pairs=10):
"""Get top trading pairs by volume"""
try:
tickers = exchange.fetch_tickers()
usdt_pairs = [
symbol for symbol in tickers.keys()
if 'USDT' in symbol and '/USDT' in symbol
]
    sorted_pairs = sorted(
        usdt_pairs,
        key=lambda x: tickers[x].get('quoteVolume', 0),
        reverse=True
    )
    
    return sorted_pairs[:num_pairs]

except Exception as e:
    st.error(f"Error fetching top pairs: {e}")
    return []
def fetch_balance(exchange):
"""Fetch account balance"""
try:
return exchange.fetch_balance()
except Exception as e:
return None
def fetch_positions(exchange):
"""Fetch open positions"""
try:
positions = exchange.fetch_positions()
return [p for p in positions if float(p.get('contracts', 0)) > 0]
except Exception as e:
return []

</details>

