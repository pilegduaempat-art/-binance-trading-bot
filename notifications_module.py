"""
Notifications Module
Sends alerts via Telegram and Discord
"""

import requests
from datetime import datetime


def send_telegram(token, chat_id, message):
    """
    Send message via Telegram bot
    
    Args:
        token (str): Telegram bot token
        chat_id (str): Telegram chat ID
        message (str): Message to send
    
    Returns:
        bool: Success status
    """
    if not token or not chat_id:
        return False
    
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        response = requests.post(url, data=data, timeout=10)
        return response.status_code == 200
    
    except Exception as e:
        print(f"Telegram error: {e}")
        return False


def send_discord(webhook, message):
    """
    Send message via Discord webhook
    
    Args:
        webhook (str): Discord webhook URL
        message (str): Message to send
    
    Returns:
        bool: Success status
    """
    if not webhook:
        return False
    
    try:
        data = {'content': message}
        response = requests.post(webhook, json=data, timeout=10)
        return response.status_code == 204
    
    except Exception as e:
        print(f"Discord error: {e}")
        return False


def format_signal_message(signal, symbol):
    """
    Format trading signal for notifications
    
    Args:
        signal (dict): Trading signal data
        symbol (str): Trading pair symbol
    
    Returns:
        str: Formatted message
    """
    timestamp = datetime.now().strftime('%H:%M:%S')
    
    message = f"""
🚨 <b>{signal['direction']} Signal</b>

💹 {symbol}
📊 Confidence: {signal['confidence']:.1f}%
⏰ {timestamp}

📍 Entry: ${signal['entry']:.4f}
🛑 SL: ${signal['sl']:.4f}
🎯 TP1: ${signal['tp1']:.4f}
🎯 TP2: ${signal['tp2']:.4f}
🎯 TP3: ${signal['tp3']:.4f}

R:R = {signal['risk_reward']:.2f}:1
Score: {signal['score']}
    """.strip()
    
    return message


def format_trade_execution_message(order, signal, symbol):
    """
    Format trade execution confirmation message
    
    Args:
        order (dict): Order information
        signal (dict): Trading signal
        symbol (str): Trading pair
    
    Returns:
        str: Formatted message
    """
    timestamp = datetime.now().strftime('%H:%M:%S')
    
    message = f"""
✅ <b>Trade Executed</b>

💹 {symbol}
📈 Direction: {signal['direction']}
⏰ {timestamp}

📍 Entry: ${signal['entry']:.4f}
💰 Size: {order.get('amount', 0):.4f}
🆔 Order ID: {order.get('id', 'N/A')}

🛑 Stop Loss: ${signal['sl']:.4f}
🎯 Take Profit: ${signal['tp3']:.4f}
    """.strip()
    
    return message


def format_position_closed_message(position, pnl, pnl_pct):
    """
    Format position closed message
    
    Args:
        position (dict): Position information
        pnl (float): Profit/Loss value
        pnl_pct (float): Profit/Loss percentage
    
    Returns:
        str: Formatted message
    """
    timestamp = datetime.now().strftime('%H:%M:%S')
    emoji = "🟢" if pnl > 0 else "🔴"
    status = "WIN" if pnl > 0 else "LOSS"
    
    message = f"""
{emoji} <b>Position Closed - {status}</b>

💹 {position['symbol']}
📈 Direction: {position['direction']}
⏰ {timestamp}

📍 Entry: ${position['entry']:.4f}
📊 Exit: ${position.get('exit_price', 0):.4f}

💰 PnL: ${pnl:.2f} ({pnl_pct:.2f}%)
    """.strip()
    
    return message


def format_daily_summary_message(trades_history, total_pnl):
    """
    Format daily trading summary
    
    Args:
        trades_history (list): List of today's trades
        total_pnl (float): Total profit/loss
    
    Returns:
        str: Formatted message
    """
    today = datetime.now().strftime('%Y-%m-%d')
    
    wins = sum(1 for t in trades_history if t.get('pnl', 0) > 0)
    losses = len(trades_history) - wins
    win_rate = (wins / len(trades_history) * 100) if trades_history else 0
    
    message = f"""
📊 <b>Daily Summary - {today}</b>

📈 Total Trades: {len(trades_history)}
🟢 Wins: {wins}
🔴 Losses: {losses}
📊 Win Rate: {win_rate:.1f}%

💰 Total PnL: ${total_pnl:.2f}
    """.strip()
    
    return message


def send_signal_notification(signal, symbol, telegram_token, telegram_chat_id, discord_webhook):
    """
    Send signal notification to all enabled channels
    
    Args:
        signal (dict): Trading signal
        symbol (str): Trading pair
        telegram_token (str): Telegram bot token
        telegram_chat_id (str): Telegram chat ID
        discord_webhook (str): Discord webhook URL
    
    Returns:
        dict: Status of each notification channel
    """
    message = format_signal_message(signal, symbol)
    discord_message = message.replace('<b>', '**').replace('</b>', '**')
    
    results = {
        'telegram': False,
        'discord': False
    }
    
    if telegram_token and telegram_chat_id:
        results['telegram'] = send_telegram(telegram_token, telegram_chat_id, message)
    
    if discord_webhook:
        results['discord'] = send_discord(discord_webhook, discord_message)
    
    return results


def send_trade_notification(order, signal, symbol, telegram_token, telegram_chat_id, discord_webhook):
    """
    Send trade execution notification
    
    Args:
        order (dict): Order information
        signal (dict): Trading signal
        symbol (str): Trading pair
        telegram_token (str): Telegram bot token
        telegram_chat_id (str): Telegram chat ID
        discord_webhook (str): Discord webhook URL
    
    Returns:
        dict: Status of each notification channel
    """
    message = format_trade_execution_message(order, signal, symbol)
    discord_message = message.replace('<b>', '**').replace('</b>', '**')
    
    results = {
        'telegram': False,
        'discord': False
    }
    
    if telegram_token and telegram_chat_id:
        results['telegram'] = send_telegram(telegram_token, telegram_chat_id, message)
    
    if discord_webhook:
        results['discord'] = send_discord(discord_webhook, discord_message)
    
    return results
