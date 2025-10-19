# 🚀 Ultimate Binance Futures Trading Bot

Advanced Multi-Strategy Trading System with Machine Learning and Auto-Trading capabilities for Binance Futures.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29.0-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

### 📊 Technical Analysis
- **35+ Technical Indicators**: EMA, RSI, MACD, Bollinger Bands, ATR, ADX, Ichimoku, and more
- **Smart Money Concepts**: Order blocks, Fair Value Gaps (FVG), Market structure
- **Volume Analysis**: CMF, MFI, OBV, Volume Profile with POC
- **Order Flow**: Real-time orderbook imbalance analysis
- **Fibonacci Levels**: Automatic retracement and extension calculations

### 🤖 Machine Learning
- Gradient Boosting Classifier for price prediction
- Feature importance analysis
- Continuous model training and optimization
- Real-time prediction integration

### 💹 Trading Features
- **Auto-Trading**: Fully automated trade execution
- **Risk Management**: Configurable risk per trade, daily loss limits
- **Position Management**: Partial take profits, trailing stops
- **Multi-timeframe**: Support for 1m, 3m, 5m, 15m, 30m, 1h timeframes
- **Multiple Pairs**: Scan top volume trading pairs automatically

### 📈 Analysis Tools
- **Backtesting Engine**: Test strategies on historical data
- **Performance Metrics**: Sharpe ratio, profit factor, win rate, max drawdown
- **Visual Analytics**: Equity curves, drawdown charts, win/loss distribution
- **Real-time Dashboard**: Monitor active positions and PnL

### 🔔 Notifications
- Telegram bot integration
- Discord webhook support
- Real-time signal alerts
- Trade execution confirmations

## 🏗️ Project Structure

```
binance-trading-bot/
│
├── app.py                  # Main application entry point
├── config.py              # Configuration and constants
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
│
├── exchange.py           # Exchange connection and data fetching
├── indicators.py         # Technical indicators calculation
├── signals.py            # Signal generation logic
├── ml_engine.py          # Machine learning model
├── trading.py            # Trade execution and management
├── backtest.py           # Backtesting engine
├── notifications.py      # Alert notifications
├── visualization.py      # Charts and visualizations
├── utils.py              # Utility functions
│
└── tabs/                 # Tab modules
    ├── __init__.py
    ├── backtest_tab.py
    ├── portfolio_tab.py
    └── analytics_tab.py
```

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/binance-trading-bot.git
cd binance-trading-bot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configuration

Create API credentials on Binance:
1. Go to Binance Account Settings
2. Create new API key
3. Enable "Futures" trading
4. Save API key and secret

### 4. Run the Application

```bash
streamlit run app.py
```

### 5. Access the App

Open your browser and navigate to:
```
http://localhost:8501
```

## 📱 Deployment to Streamlit Cloud

### 1. Push to GitHub

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### 2. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set main file path: `app.py`
6. Click "Deploy"

### 3. Configure Secrets

In Streamlit Cloud dashboard:
1. Go to App Settings → Secrets
2. Add your secrets (optional):

```toml
# Not recommended to store API keys here
# Use the UI inputs instead for security
```

## ⚙️ Configuration

### API Settings
- **API Key**: Your Binance API key
- **API Secret**: Your Binance API secret
- **Testnet**: Enable to use Binance Futures testnet

### Auto-Trading Settings
- **Risk per Trade**: 0.5% - 5% of balance
- **Daily Loss Limit**: Maximum daily loss percentage
- **Max Positions**: Maximum concurrent positions
- **Trailing Stop**: Enable dynamic stop loss
- **Partial TP**: Take profits at multiple levels

### Scan Settings
- **Timeframe**: Chart timeframe for analysis
- **Pairs to Track**: Number of top volume pairs to scan
- **Min Confidence**: Minimum signal confidence (50-95%)
- **Auto Rescan**: Automatic periodic rescanning

## 📊 Usage Guide

### Scanning for Signals

1. Enter your API credentials in the sidebar
2. Configure scan settings
3. Click "🔍 Scan" button
4. Review generated signals with charts
5. Execute trades manually or enable auto-trading

### Auto-Trading

1. Enable "Auto-Trading" in sidebar
2. Configure risk parameters
3. Signals meeting criteria will be auto-executed
4. Monitor positions in Portfolio tab

### Backtesting

1. Go to "Backtest" tab
2. Select symbol, timeframe, and period
3. Click "Run Backtest"
4. Review performance metrics and charts

### ML Model Training

1. Click "🤖 Train ML" in sidebar
2. Wait for training to complete
3. ML predictions will be integrated into signals
4. View feature importance in Analytics tab

## 🛡️ Risk Warning

**⚠️ IMPORTANT**: Cryptocurrency trading involves substantial risk of loss. This bot is for educational purposes only.

- Never invest more than you can afford to lose
- Always test on testnet first
- Use proper risk management
- Monitor your positions regularly
- No guarantee of profits

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

For questions or support, please open an issue on GitHub.

## 🙏 Acknowledgments

- CCXT library for exchange connectivity
- TA-Lib for technical analysis
- Plotly for interactive charts
- Streamlit for the web interface

---

**Disclaimer**: This software is for educational purposes only. Use at your own risk. The authors and contributors are not responsible for any financial losses incurred through the use of this software.
