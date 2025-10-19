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
