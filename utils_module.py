"""
Utility Functions Module
Common helper functions used across the application
"""

import streamlit as st
from datetime import datetime, timedelta
from config import DEFAULT_SESSION_STATE


def init_session_state():
    """
    Initialize Streamlit session state with default values
    """
    for key, value in DEFAULT_SESSION_STATE.items():
        if key not in st.session_state:
            st.session_state[key] = value


def format_number(value, decimals=2):
    """
    Format number with thousand separators
    
    Args:
        value (float): Number to format
        decimals (int): Number of decimal places
    
    Returns:
        str: Formatted number string
    """
    return f"{value:,.{decimals}f}"


def format_percentage(value, decimals=2):
    """
    Format percentage value
    
    Args:
        value (float): Percentage value
        decimals (int): Number of decimal places
    
    Returns:
        str: Formatted percentage string
    """
    return f"{value:.{decimals}f}%"


def format_currency(value, symbol="$", decimals=2):
    """
    Format currency value
    
    Args:
        value (float): Currency value
        symbol (str): Currency symbol
        decimals (int): Number of decimal places
    
    Returns:
        str: Formatted currency string
    """
    return f"{symbol}{value:,.{decimals}f}"


def get_timeframe_minutes(timeframe):
    """
    Convert timeframe string to minutes
    
    Args:
        timeframe (str): Timeframe string (e.g., '5m', '1h')
    
    Returns:
        int: Number of minutes
    """
    mapping = {
        '1m': 1,
        '3m': 3,
        '5m': 5,
        '15m': 15,
        '30m': 30,
        '1h': 60,
        '4h': 240,
        '1d': 1440
    }
    return mapping.get(timeframe, 5)


def calculate_time_ago(timestamp):
    """
    Calculate human-readable time difference
    
    Args:
        timestamp (datetime): Timestamp to compare
    
    Returns:
        str: Human-readable time difference
    """
    if timestamp is None:
        return "Never"
    
    now = datetime.now()
    diff = now - timestamp
    
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return f"{int(seconds)} seconds ago"
    elif seconds < 3600:
        return f"{int(seconds / 60)} minutes ago"
    elif seconds < 86400:
        return f"{int(seconds / 3600)} hours ago"
    else:
        return f"{int(seconds / 86400)} days ago"


def validate_api_credentials(api_key, api_secret):
    """
    Validate API credentials format
    
    Args:
        api_key (str): API key
        api_secret (str): API secret
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if not api_key or not api_secret:
        return False, "API key and secret are required"
    
    if len(api_key) < 20:
        return False, "API key seems too short"
    
    if len(api_secret) < 20:
        return False, "API secret seems too short"
    
    return True, ""


def safe_divide(numerator, denominator, default=0):
    """
    Safely divide two numbers
    
    Args:
        numerator (float): Numerator
        denominator (float): Denominator
        default: Default value if division fails
    
    Returns:
        float: Result of division or default
    """
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except:
        return default


def truncate_string(text, max_length=50):
    """
    Truncate string to maximum length
    
    Args:
        text (str): String to truncate
        max_length (int): Maximum length
    
    Returns:
        str: Truncated string
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def get_color_for_value(value, neutral_threshold=0):
    """
    Get color based on value (green for positive, red for negative)
    
    Args:
        value (float): Value to evaluate
        neutral_threshold (float): Threshold for neutral color
    
    Returns:
        str: Color string
    """
    if value > neutral_threshold:
        return "#00ff00"  # Green
    elif value < -neutral_threshold:
        return "#ff0000"  # Red
    else:
        return "#808080"  # Gray


def create_progress_message(current, total, prefix=""):
    """
    Create progress message string
    
    Args:
        current (int): Current count
        total (int): Total count
        prefix (str): Message prefix
    
    Returns:
        str: Progress message
    """
    percentage = (current / total * 100) if total > 0 else 0
    return f"{prefix} ({current}/{total}) - {percentage:.1f}%"


def is_market_open(symbol="BTC/USDT"):
    """
    Check if crypto market is open (always true for crypto)
    
    Args:
        symbol (str): Trading pair symbol
    
    Returns:
        bool: True (crypto markets are 24/7)
    """
    return True


def get_risk_level(risk_pct):
    """
    Get risk level description
    
    Args:
        risk_pct (float): Risk percentage
    
    Returns:
        tuple: (level_name, color)
    """
    if risk_pct <= 1:
        return ("Low", "#00ff00")
    elif risk_pct <= 2:
        return ("Medium", "#ffff00")
    elif risk_pct <= 3:
        return ("High", "#ff8800")
    else:
        return ("Very High", "#ff0000")


def sanitize_symbol(symbol):
    """
    Sanitize trading pair symbol
    
    Args:
        symbol (str): Raw symbol
    
    Returns:
        str: Sanitized symbol
    """
    return symbol.replace("/", "").replace(":", "").upper()


def parse_timeframe(timeframe_str):
    """
    Parse timeframe string to value and unit
    
    Args:
        timeframe_str (str): Timeframe string (e.g., '5m', '1h')
    
    Returns:
        tuple: (value, unit)
    """
    import re
    match = re.match(r'(\d+)([mhd])', timeframe_str.lower())
    if match:
        return int(match.group(1)), match.group(2)
    return None, None


def calculate_position_size(balance, risk_pct, entry_price, sl_price):
    """
    Calculate position size based on risk parameters
    
    Args:
        balance (float): Account balance
        risk_pct (float): Risk percentage
        entry_price (float): Entry price
        sl_price (float): Stop loss price
    
    Returns:
        float: Position size
    """
    risk_amount = balance * (risk_pct / 100)
    risk_distance = abs(entry_price - sl_price)
    
    if risk_distance == 0:
        return 0
    
    return risk_amount / risk_distance


def merge_dicts(*dicts):
    """
    Merge multiple dictionaries
    
    Args:
        *dicts: Variable number of dictionaries
    
    Returns:
        dict: Merged dictionary
    """
    result = {}
    for d in dicts:
        if d:
            result.update(d)
    return result


def chunk_list(lst, chunk_size):
    """
    Split list into chunks
    
    Args:
        lst (list): List to split
        chunk_size (int): Size of each chunk
    
    Returns:
        list: List of chunks
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]
