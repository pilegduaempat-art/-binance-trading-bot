"""
Configuration Module
Manages application settings and constants
"""

# Application Settings
APP_CONFIG = {
    'page_title': "Ultimate Trading Bot",
    'page_icon': "🚀",
    'layout': "wide",
    'initial_sidebar_state': "expanded"
}

# Default Session State Values
DEFAULT_SESSION_STATE = {
    'api_key': '',
    'api_secret': '',
    'telegram_token': '',
    'telegram_chat_id': '',
    'discord_webhook': '',
    'auto_trading_enabled': False,
    'max_positions': 3,
    'risk_per_trade': 2.0,
    'daily_loss_limit': 5.0,
    'use_trailing_stop': True,
    'partial_tp': True,
    'trades_history': [],
    'active_positions': [],
    'total_pnl': 0.0,
    'ml_model': None,
    'scaler': None,
    'backtest_results': None,
    'last_scan': None,
    'auto_rescan': False,
    'rescan_interval': 300,
    'scan_counter': 0,
    'last_signals': []
}

# Trading Settings
TRADING_CONFIG = {
    'timeframes': ['1m', '3m', '5m', '15m', '30m', '1h'],
    'default_timeframe': '5m',
    'default_limit': 500,
    'min_candles': 200,
    'orderbook_depth': 20
}

# Risk Management
RISK_CONFIG = {
    'min_risk_per_trade': 0.5,
    'max_risk_per_trade': 5.0,
    'default_risk_per_trade': 2.0,
    'min_daily_loss_limit': 1.0,
    'max_daily_loss_limit': 20.0,
    'default_daily_loss_limit': 5.0,
    'max_position_size_pct': 10.0
}

# Signal Generation
SIGNAL_CONFIG = {
    'min_confidence': 50,
    'max_confidence': 95,
    'default_confidence': 70,
    'min_score_long': 6,
    'min_score_short': -6,
    'atr_multiplier_sl': 2.5,
    'atr_multiplier_tp1': 1.5,
    'atr_multiplier_tp2': 3.0,
    'atr_multiplier_tp3': 5.0
}

# Machine Learning
ML_CONFIG = {
    'n_estimators': 100,
    'learning_rate': 0.1,
    'max_depth': 5,
    'random_state': 42,
    'test_size': 0.2,
    'min_samples': 100,
    'future_periods': 5,
    'target_return': 0.005
}

# Backtesting
BACKTEST_CONFIG = {
    'initial_balance': 10000,
    'risk_per_trade_pct': 2.0,
    'min_candles': 200
}

# Fibonacci Levels
FIBONACCI_LEVELS = {
    'retracements': [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0],
    'extensions': [1.272, 1.618]
}

# Technical Indicators Windows
INDICATOR_WINDOWS = {
    'ema_fast': 9,
    'ema_medium': 21,
    'ema_slow': 50,
    'ema_very_slow': 100,
    'sma_long': 200,
    'rsi': 14,
    'macd_fast': 12,
    'macd_slow': 26,
    'macd_signal': 9,
    'stoch': 14,
    'bb': 20,
    'atr': 14,
    'volume_sma': 20,
    'roc': 12
}

# RSI Levels
RSI_LEVELS = {
    'oversold': 30,
    'overbought': 70,
    'extreme_oversold': 20,
    'extreme_overbought': 80
}

# ADX Levels
ADX_LEVELS = {
    'strong_trend': 25,
    'very_strong_trend': 40
}

# Volume Threshold
VOLUME_CONFIG = {
    'high_volume_ratio': 2.0,
    'cmf_bullish': 0.15,
    'cmf_bearish': -0.15,
    'mfi_oversold': 20,
    'mfi_overbought': 80
}

# Orderbook Analysis
ORDERBOOK_CONFIG = {
    'imbalance_bullish': 0.3,
    'imbalance_bearish': -0.3
}

# Chart Settings
CHART_CONFIG = {
    'height': 1000,
    'template': 'plotly_dark',
    'row_heights': [0.5, 0.15, 0.15, 0.2]
}

# Custom CSS Styling
CUSTOM_CSS = """
<style>
    .stMetric {
        background-color: #1e1e1e;
        padding: 10px;
        border-radius: 5px;
    }
    .profit {color: #00ff00;}
    .loss {color: #ff0000;}
    .signal-box {
        border: 2px solid #4CAF50;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
"""
