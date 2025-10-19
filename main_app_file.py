"""
Binance Futures Trading Bot - Main Application
Ultimate Multi-Strategy Trading System with ML & Auto-Trading
"""

import streamlit as st
import time
import warnings
from datetime import datetime

# Import custom modules
from config import APP_CONFIG, CUSTOM_CSS
from utils import init_session_state, format_currency, format_percentage, calculate_time_ago
from exchange import (
    get_exchange, fetch_ohlcv, fetch_orderbook, 
    fetch_funding_rate, get_top_volume_pairs, 
    fetch_balance, fetch_positions
)
from indicators import calculate_indicators
from signals import generate_comprehensive_signal
from ml_engine import train_ml_model, predict_with_ml
from trading import execute_trade, calculate_position_pnl, check_daily_loss_limit
from backtest import backtest_strategy
from notifications import send_signal_notification, send_trade_notification
from visualization import (
    create_advanced_chart, create_equity_curve_chart,
    create_drawdown_chart, create_win_loss_chart
)

# Suppress warnings
warnings.filterwarnings('ignore')

# ==================== PAGE CONFIG ====================
st.set_page_config(**APP_CONFIG)

# Apply custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Initialize session state
init_session_state()


# ==================== SIDEBAR ====================
def render_sidebar():
    """Render sidebar configuration"""
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Settings
        with st.expander("🔑 API Settings", expanded=True):
            api_key = st.text_input(
                "Binance API Key",
                type="password",
                value=st.session_state.api_key
            )
            api_secret = st.text_input(
                "Binance Secret",
                type="password",
                value=st.session_state.api_secret
            )
            testnet = st.checkbox("Use Testnet", value=True)
        
        # Notifications
        with st.expander("📱 Notifications"):
            telegram_token = st.text_input(
                "Telegram Token",
                type="password",
                value=st.session_state.telegram_token
            )
            telegram_chat_id = st.text_input(
                "Chat ID",
                value=st.session_state.telegram_chat_id
            )
            discord_webhook = st.text_input(
                "Discord Webhook",
                type="password",
                value=st.session_state.discord_webhook
            )
        
        # Auto-Trading Settings
        with st.expander("🤖 Auto-Trading Settings"):
            auto_trading = st.checkbox(
                "Enable Auto-Trading",
                value=st.session_state.auto_trading_enabled
            )
            st.warning("⚠️ Auto-trading will execute real trades!")
            
            max_positions = st.number_input(
                "Max Concurrent Positions",
                1, 10,
                st.session_state.max_positions
            )
            risk_per_trade = st.slider(
                "Risk per Trade (%)",
                0.5, 5.0,
                st.session_state.risk_per_trade,
                0.1
            )
            daily_loss_limit = st.slider(
                "Daily Loss Limit (%)",
                1.0, 20.0,
                st.session_state.daily_loss_limit,
                0.5
            )
            use_trailing_stop = st.checkbox(
                "Use Trailing Stop",
                value=st.session_state.use_trailing_stop
            )
            partial_tp = st.checkbox(
                "Partial Take Profits",
                value=st.session_state.partial_tp
            )
            
            # Update session state
            st.session_state.update({
                'auto_trading_enabled': auto_trading,
                'max_positions': max_positions,
                'risk_per_trade': risk_per_trade,
                'daily_loss_limit': daily_loss_limit,
                'use_trailing_stop': use_trailing_stop,
                'partial_tp': partial_tp
            })
        
        # Scan Settings
        with st.expander("📊 Scan Settings"):
            timeframe = st.selectbox(
                "Timeframe",
                ['1m', '3m', '5m', '15m', '30m', '1h'],
                index=2
            )
            num_pairs = st.slider("Pairs to Track", 5, 30, 10)
            min_confidence = st.slider("Min Confidence (%)", 50, 95, 70)
            
            st.markdown("---")
            auto_rescan = st.checkbox(
                "🔄 Auto Rescan",
                value=st.session_state.get('auto_rescan', False)
            )
            rescan_interval = st.number_input(
                "Rescan Interval (seconds)",
                60, 3600, 300, 30
            )
            
            st.session_state['auto_rescan'] = auto_rescan
            st.session_state['rescan_interval'] = rescan_interval
            
            if auto_rescan:
                st.success(f"✅ Auto-rescan every {rescan_interval}s")
            else:
                st.info("⏸️ Auto-rescan disabled")
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        scan_btn = col1.button("🔍 Scan", type="primary", use_container_width=True)
        train_ml_btn = col2.button("🤖 Train ML", use_container_width=True)
        
        return {
            'api_key': api_key,
            'api_secret': api_secret,
            'testnet': testnet,
            'telegram_token': telegram_token,
            'telegram_chat_id': telegram_chat_id,
            'discord_webhook': discord_webhook,
            'timeframe': timeframe,
            'num_pairs': num_pairs,
            'min_confidence': min_confidence,
            'scan_btn': scan_btn,
            'train_ml_btn': train_ml_btn
        }


# ==================== DASHBOARD TAB ====================
def render_dashboard(config):
    """Render dashboard tab"""
    if not config['api_key'] or not config['api_secret']:
        st.info("👈 Enter API credentials in sidebar to start")
        return
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_trades = len(st.session_state.trades_history)
    wins = sum(1 for t in st.session_state.trades_history if t.get('pnl', 0) > 0)
    win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
    
    col1.metric(
        "Total PnL",
        format_currency(st.session_state.total_pnl),
        delta=format_percentage((st.session_state.total_pnl / 10000) * 100)
    )
    col2.metric("Active Positions", len(st.session_state.active_positions))
    col3.metric("Total Trades", total_trades)
    col4.metric("Win Rate", format_percentage(win_rate))
    
    st.markdown("---")
    
    if st.session_state.last_scan:
        st.success(f"✅ Last scan: {st.session_state.last_scan.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Active Signals and Performance
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Active Signals")
        if st.session_state.active_positions:
            for pos in st.session_state.active_positions:
                with st.container():
                    st.markdown(f"**{pos['symbol']}** - {pos['direction']}")
                    st.caption(
                        f"Entry: ${pos['entry']:.4f} | "
                        f"Current PnL: {pos.get('current_pnl', 0):.2f}%"
                    )
        else:
            st.info("No active positions")
    
    with col2:
        st.subheader("📈 Recent Performance")
        if st.session_state.trades_history:
            recent = st.session_state.trades_history[-10:]
            recent_wins = sum(1 for t in recent if t.get('pnl', 0) > 0)
            st.metric("Last 10 Trades", f"{recent_wins}/10 wins")
            
            pnl_sum = sum(t.get('pnl', 0) for t in recent)
            st.metric("Recent PnL", format_currency(pnl_sum))


# ==================== SIGNALS TAB ====================
def render_signals_tab(config):
    """Render signals scanning tab"""
    # Auto-rescan logic
    if st.session_state.auto_rescan:
        handle_auto_rescan(config)
    
    # Manual scan or auto-scan triggered
    if config['scan_btn'] or st.session_state.get('trigger_scan', False):
        st.session_state['trigger_scan'] = False
        run_market_scan(config)
    
    # Display last signals
    elif st.session_state.last_signals:
        display_saved_signals()


def handle_auto_rescan(config):
    """Handle auto-rescan timer"""
    current_time = datetime.now()
    
    if st.session_state.last_scan:
        time_diff = (current_time - st.session_state.last_scan).total_seconds()
        time_remaining = st.session_state.rescan_interval - time_diff
        
        if time_remaining > 0:
            col1, col2 = st.columns([3, 1])
            col1.info(f"⏳ Next auto-scan in: {int(time_remaining)}s")
            
            if col2.button("⏭️ Skip"):
                st.session_state.last_scan = None
                st.rerun()
            
            # Auto-refresh
            time.sleep(1)
            st.rerun()
        else:
            # Trigger scan
            st.session_state['trigger_scan'] = True
            st.session_state.scan_counter += 1
            st.info(f"🔄 Auto-scan #{st.session_state.scan_counter} started...")
    else:
        if st.session_state.get('trigger_scan'):
            st.session_state.scan_counter = 1


def run_market_scan(config):
    """Execute market scanning"""
    # Save credentials to session
    st.session_state.update({
        'api_key': config['api_key'],
        'api_secret': config['api_secret'],
        'telegram_token': config['telegram_token'],
        'telegram_chat_id': config['telegram_chat_id'],
        'discord_webhook': config['discord_webhook']
    })
    
    with st.spinner("🔄 Scanning markets..."):
        exchange = get_exchange(config['api_key'], config['api_secret'], config['testnet'])
        
        if not exchange:
            st.error("Failed to connect to exchange")
            return
        
        try:
            # Get top pairs
            sorted_pairs = get_top_volume_pairs(exchange, config['num_pairs'])
            
            signals_found = []
            progress = st.progress(0)
            status = st.empty()
            
            # Scan each pair
            for idx, symbol in enumerate(sorted_pairs):
                status.text(f"Analyzing {symbol}... ({idx + 1}/{len(sorted_pairs)})")
                progress.progress((idx + 1) / len(sorted_pairs))
                
                # Fetch data
                df = fetch_ohlcv(
                    config['api_key'],
                    config['api_secret'],
                    symbol,
                    config['timeframe'],
                    500
                )
                
                if df is None or len(df) < 200:
                    continue
                
                # Calculate indicators
                df = calculate_indicators(df)
                orderbook = fetch_orderbook(exchange, symbol)
                funding = fetch_funding_rate(exchange, symbol)
                
                # ML Prediction
                ml_pred = None
                if st.session_state.ml_model:
                    ml_pred = predict_with_ml(
                        df,
                        st.session_state.ml_model,
                        st.session_state.scaler
                    )
                
                # Generate signal
                signal = generate_comprehensive_signal(df, orderbook, funding, ml_pred)
                
                if signal and signal['confidence'] >= config['min_confidence']:
                    signal['symbol'] = symbol
                    signal['timestamp'] = datetime.now()
                    signal['df'] = df
                    signals_found.append(signal)
            
            progress.empty()
            status.empty()
            st.session_state.last_scan = datetime.now()
            st.session_state.last_signals = signals_found
            
            # Display results
            display_scan_results(signals_found, config)
        
        except Exception as e:
            st.error(f"Scan error: {e}")


def display_scan_results(signals_found, config):
    """Display scanned signals"""
    if not signals_found:
        st.info(
            f"⏳ No signals meeting criteria (Scan #{st.session_state.scan_counter}). "
            "Try adjusting confidence threshold."
        )
        return
    
    st.success(
        f"🎯 Found {len(signals_found)} high-quality signals! "
        f"(Scan #{st.session_state.scan_counter})"
    )
    
    # Sort by confidence
    signals_found.sort(key=lambda x: x['confidence'], reverse=True)
    
    # Display each signal
    for signal in signals_found:
        display_signal_card(signal, config)


def display_signal_card(signal, config):
    """Display individual signal card"""
    emoji = '🟢' if signal['direction'] == 'LONG' else '🔴'
    
    with st.expander(
        f"{emoji} {signal['symbol']} - {signal['direction']} "
        f"({signal['confidence']:.1f}% confidence)",
        expanded=True
    ):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Chart
            chart = create_advanced_chart(signal['df'], signal)
            st.plotly_chart(chart, use_container_width=True)
        
        with col2:
            # Trade setup
            st.markdown("### 📊 Trade Setup")
            st.metric("Entry", f"${signal['entry']:.4f}")
            st.metric(
                "Stop Loss",
                f"${signal['sl']:.4f}",
                delta=f"-{abs((signal['entry'] - signal['sl']) / signal['entry'] * 100):.2f}%"
            )
            st.metric(
                "TP1",
                f"${signal['tp1']:.4f}",
                delta=f"+{abs((signal['tp1'] - signal['entry']) / signal['entry'] * 100):.2f}%"
            )
            st.metric(
                "TP2",
                f"${signal['tp2']:.4f}",
                delta=f"+{abs((signal['tp2'] - signal['entry']) / signal['entry'] * 100):.2f}%"
            )
            st.metric(
                "TP3",
                f"${signal['tp3']:.4f}",
                delta=f"+{abs((signal['tp3'] - signal['entry']) / signal['entry'] * 100):.2f}%"
            )
            st.metric("Risk/Reward", f"{signal['risk_reward']:.2f}:1")
            
            st.markdown("---")
            st.markdown("### 📈 Signal Strength")
            
            for key, val in signal['signals'].items():
                color = "🟢" if val > 0 else "🔴" if val < 0 else "⚪"
                st.write(f"{color} {key.title()}: **{val}**")
            
            # Execute button
            if (st.session_state.auto_trading_enabled and 
                len(st.session_state.active_positions) < st.session_state.max_positions):
                
                if st.button(
                    f"✅ Execute {signal['direction']}",
                    key=f"exec_{signal['symbol']}_{st.session_state.scan_counter}"
                ):
                    execute_signal_trade(signal, config)
        
        # Send notifications
        send_signal_notification(
            signal,
            signal['symbol'],
            config['telegram_token'],
            config['telegram_chat_id'],
            config['discord_webhook']
        )


def execute_signal_trade(signal, config):
    """Execute trade from signal"""
    exchange = get_exchange(config['api_key'], config['api_secret'], config['testnet'])
    
    if exchange:
        order = execute_trade(exchange, signal, signal['symbol'], st.session_state)
        
        if order:
            st.success("Trade executed!")
            st.session_state.active_positions.append({
                'symbol': signal['symbol'],
                'direction': signal['direction'],
                'entry': signal['entry'],
                'order_id': order['id']
            })


def display_saved_signals():
    """Display previously scanned signals"""
    st.info(
        f"📊 Showing last scan results "
        f"({st.session_state.scan_counter} scans completed)"
    )
    
    for signal in st.session_state.last_signals:
        emoji = '🟢' if signal['direction'] == 'LONG' else '🔴'
        
        with st.expander(
            f"{emoji} {signal['symbol']} - {signal['direction']} "
            f"({signal['confidence']:.1f}% confidence)"
        ):
            col1, col2, col3 = st.columns(3)
            col1.metric("Entry", f"${signal['entry']:.4f}")
            col2.metric("Stop Loss", f"${signal['sl']:.4f}")
            col3.metric("TP3", f"${signal['tp3']:.4f}")
            st.caption(
                f"⏰ Scanned at: {signal['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}"
            )


# ==================== MAIN FUNCTION ====================
def main():
    """Main application function"""
    st.title("🚀 Ultimate Binance Futures Trading Bot")
    st.markdown("**Advanced Multi-Strategy Trading System with ML & Auto-Trading**")
    
    # Render sidebar and get config
    config = render_sidebar()
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard",
        "📈 Signals",
        "🔙 Backtest",
        "💼 Portfolio",
        "📚 Analytics"
    ])
    
    with tab1:
        render_dashboard(config)
    
    with tab2:
        render_signals_tab(config)
    
    with tab3:
        from tabs.backtest_tab import render_backtest_tab
        render_backtest_tab(config)
    
    with tab4:
        from tabs.portfolio_tab import render_portfolio_tab
        render_portfolio_tab(config)
    
    with tab5:
        from tabs.analytics_tab import render_analytics_tab
        render_analytics_tab(config)


if __name__ == "__main__":
    main()