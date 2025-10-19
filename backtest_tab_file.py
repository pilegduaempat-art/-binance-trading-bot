"""
Backtest Tab Module
Handles strategy backtesting interface
"""

import streamlit as st
from exchange import fetch_ohlcv
from indicators import calculate_indicators
from signals import generate_comprehensive_signal
from backtest import backtest_strategy
from visualization import create_equity_curve_chart, create_drawdown_chart, create_win_loss_chart
from utils import format_currency, format_percentage


def render_backtest_tab(config):
    """Render backtesting tab"""
    st.subheader("🔙 Strategy Backtesting")
    
    # Backtest configuration
    col1, col2, col3 = st.columns(3)
    
    bt_symbol = col1.selectbox(
        "Symbol",
        ['BTC/USDT:USDT', 'ETH/USDT:USDT', 'BNB/USDT:USDT', 'SOL/USDT:USDT']
    )
    bt_timeframe = col2.selectbox(
        "Timeframe",
        ['5m', '15m', '1h', '4h'],
        key='bt_tf'
    )
    bt_period = col3.number_input("Candles", 500, 2000, 1000)
    
    if st.button("🔄 Run Backtest", type="primary"):
        run_backtest(config, bt_symbol, bt_timeframe, bt_period)
    
    # Display saved backtest results
    if st.session_state.backtest_results:
        display_backtest_results(st.session_state.backtest_results)


def run_backtest(config, symbol, timeframe, period):
    """Execute backtest"""
    with st.spinner("Running backtest..."):
        # Fetch historical data
        df = fetch_ohlcv(
            config['api_key'],
            config['api_secret'],
            symbol,
            timeframe,
            period
        )
        
        if df is None:
            st.error("Failed to fetch data")
            return
        
        # Calculate indicators
        df = calculate_indicators(df)
        
        # Define signal generation function
        def signal_gen(data):
            return generate_comprehensive_signal(data, None, None)
        
        # Run backtest
        results = backtest_strategy(df, signal_gen)
        
        if results:
            st.session_state.backtest_results = results
            st.success("✅ Backtest Complete!")
        else:
            st.warning("No trades generated in backtest")


def display_backtest_results(results):
    """Display backtest results"""
    st.markdown("---")
    st.subheader("📊 Backtest Results")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Trades", results['total_trades'])
    col2.metric("Win Rate", format_percentage(results['win_rate']))
    col3.metric("Profit Factor", f"{results['profit_factor']:.2f}")
    col4.metric("Total Return", format_percentage(results['total_return']))
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Sharpe Ratio", f"{results['sharpe_ratio']:.2f}")
    col2.metric("Max Drawdown", format_percentage(results['max_drawdown']))
    col3.metric("Avg Win", format_currency(results['avg_win']))
    col4.metric("Avg Loss", format_currency(results['avg_loss']))
    
    # Additional metrics
    st.markdown("### 📈 Additional Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Final Balance", format_currency(results['final_balance']))
    col2.metric("Avg Duration", f"{results['avg_duration']:.1f} candles")
    col3.metric("Expectancy", format_currency(results['expectancy']))
    
    # Charts
    st.markdown("---")
    
    # Equity curve
    st.markdown("### 💰 Equity Curve")
    equity_chart = create_equity_curve_chart(results['equity_curve'])
    st.plotly_chart(equity_chart, use_container_width=True)
    
    # Drawdown chart
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📉 Drawdown")
        dd_chart = create_drawdown_chart(results['equity_curve'])
        st.plotly_chart(dd_chart, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Win/Loss Distribution")
        wl_chart = create_win_loss_chart(results['trades'])
        st.plotly_chart(wl_chart, use_container_width=True)
    
    # Trade history
    st.markdown("---")
    st.markdown("### 📋 Trade History")
    
    if st.checkbox("Show Trade Details"):
        import pandas as pd
        
        trades_df = pd.DataFrame(results['trades'])
        trades_df['exit_time'] = pd.to_datetime(trades_df['exit_time'])
        trades_df['entry_time'] = pd.to_datetime(trades_df['entry_time'])
        
        st.dataframe(
            trades_df,
            use_container_width=True,
            hide_index=True
        )
