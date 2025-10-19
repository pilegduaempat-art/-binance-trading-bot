"""
Analytics Tab Module
Advanced analytics and ML model management
"""

import streamlit as st
from exchange import fetch_ohlcv
from indicators import calculate_indicators
from ml_engine import train_ml_model, get_feature_importance
from utils import format_percentage


def render_analytics_tab(config):
    """Render analytics and ML tab"""
    st.subheader("📚 Advanced Analytics")
    
    # ML Model Section
    render_ml_section(config)
    
    st.markdown("---")
    
    # Feature Information
    render_features_section()
    
    st.markdown("---")
    
    # Strategy Information
    render_strategy_info()


def render_ml_section(config):
    """Render ML model section"""
    st.markdown("### 🤖 Machine Learning Model")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.session_state.ml_model:
            st.success("✅ ML Model Active")
            
            # Display feature importance if available
            if st.button("Show Feature Importance"):
                display_feature_importance()
        else:
            st.warning("⚠️ No ML model trained")
            st.info("Click 'Train ML' in the sidebar to enable AI predictions")
    
    with col2:
        if st.button("🔄 Retrain Model", use_container_width=True):
            train_model(config)


def train_model(config):
    """Train ML model"""
    with st.spinner("🤖 Training ML model..."):
        df = fetch_ohlcv(
            config['api_key'],
            config['api_secret'],
            'BTC/USDT:USDT',
            '5m',
            2000
        )
        
        if df is None:
            st.error("Failed to fetch data")
            return
        
        df = calculate_indicators(df)
        model, scaler, accuracy = train_ml_model(df)
        
        if model:
            st.session_state.ml_model = model
            st.session_state.scaler = scaler
            st.success(f"✅ Model trained! Accuracy: {format_percentage(accuracy * 100)}")
            st.rerun()
        else:
            st.error("Training failed")


def display_feature_importance():
    """Display ML feature importance"""
    feature_names = [
        'rsi', 'macd_diff', 'stoch_k', 'bb_width', 'atr',
        'cmf', 'mfi', 'adx', 'roc', 'cci', 'williams_r',
        'volume_ratio', 'ema_9', 'ema_21', 'ema_50'
    ]
    
    importance_df = get_feature_importance(st.session_state.ml_model, feature_names)
    
    if importance_df is not None:
        st.markdown("#### 📊 Feature Importance")
        
        import plotly.graph_objects as go
        
        fig = go.Figure(
            go.Bar(
                x=importance_df['importance'],
                y=importance_df['feature'],
                orientation='h',
                marker=dict(color='cyan')
            )
        )
        
        fig.update_layout(
            title="ML Model Feature Importance",
            xaxis_title="Importance",
            yaxis_title="Feature",
            template='plotly_dark',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)


def render_features_section():
    """Render features information"""
    st.markdown("### 📊 Features Included")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### Technical Indicators
        - ✅ EMA (9, 21, 50, 100, 200)
        - ✅ RSI with divergence detection
        - ✅ MACD with histogram
        - ✅ Stochastic Oscillator
        - ✅ Bollinger Bands
        - ✅ ATR (Average True Range)
        - ✅ ADX (Trend Strength)
        - ✅ Ichimoku Cloud
        - ✅ ROC, CCI, Williams %R
        """)
    
    with col2:
        st.markdown("""
        #### Advanced Analysis
        - ✅ Smart Money Concepts (SMC)
        - ✅ Order Block Detection
        - ✅ Fair Value Gaps (FVG)
        - ✅ Volume Profile & POC
        - ✅ Order Flow Analysis
        - ✅ Market Structure Detection
        - ✅ Fibonacci Levels
        - ✅ Chaikin Money Flow
        - ✅ Money Flow Index
        """)


def render_strategy_info():
    """Render strategy information"""
    st.markdown("### 🎯 Strategy Components")
    
    strategies = [
        {
            'name': 'Trend Following',
            'description': 'EMA alignment, ADX strength, market structure',
            'weight': '30%'
        },
        {
            'name': 'Momentum',
            'description': 'RSI, MACD, Stochastic crossovers and divergences',
            'weight': '25%'
        },
        {
            'name': 'Volume Analysis',
            'description': 'CMF, MFI, OBV, volume ratio confirmation',
            'weight': '20%'
        },
        {
            'name': 'Market Structure',
            'description': 'Order blocks, FVG, higher highs/lower lows',
            'weight': '15%'
        },
        {
            'name': 'Order Flow',
            'description': 'Bid/ask imbalance, orderbook depth',
            'weight': '10%'
        }
    ]
    
    for strategy in strategies:
        with st.expander(f"**{strategy['name']}** - Weight: {strategy['weight']}"):
            st.write(strategy['description'])
    
    st.markdown("---")
    
    st.markdown("""
    ### ⚙️ Risk Management Features
    - 🛡️ Configurable risk per trade (0.5% - 5%)
    - 🚫 Daily loss limit protection
    - 📊 Partial take profit system (30/30/40)
    - 📈 Trailing stop loss
    - 🎯 Dynamic position sizing
    - ⚖️ Risk/Reward ratio filtering
    - 🔄 Maximum concurrent positions limit
    """)
    
    st.markdown("---")
    
    st.markdown("""
    ### 📱 Notification Channels
    - 📲 Telegram bot integration
    - 💬 Discord webhook support
    - 🔔 Real-time signal alerts
    - ✅ Trade execution confirmations
    - 📊 Daily performance summaries
    """)
    
    st.markdown("---")
    
    st.info("""
    💡 **Pro Tip**: The bot combines multiple strategies and uses a scoring system. 
    Signals are only generated when the combined score exceeds the threshold, 
    ensuring high-quality trade setups with better risk/reward ratios.
    """)
