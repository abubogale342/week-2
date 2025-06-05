import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from datetime import datetime, timedelta
import talib
import yfinance as yf
from pynance.utils import get_returns, get_drawdowns

# Set style for plots
plt.style.use('ggplot')
sns.set_palette("husl")

def load_stock_data(symbol, start_date=None, end_date=None):
    """
    Load stock data using yfinance.
    
    Args:
        symbol (str): Stock symbol (e.g., 'AAPL')
        start_date (str): Start date in 'YYYY-MM-DD' format
        end_date (str): End date in 'YYYY-MM-DD' format
        
    Returns:
        pd.DataFrame: DataFrame with stock data
    """
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
    if start_date is None:
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        
    print(f"Downloading {symbol} data from {start_date} to {end_date}...")
    df = yf.download(symbol, start=start_date, end=end_date, progress=False)
    
    if df.empty:
        raise ValueError(f"No data found for {symbol}")
        
    return df

def add_technical_indicators(df):
    """Add technical indicators to the DataFrame using TA-Lib."""
    # Make a copy to avoid SettingWithCopyWarning
    df = df.copy()
    
    # Moving Averages
    df['SMA_20'] = talib.SMA(df['Close'], timeperiod=20)
    df['SMA_50'] = talib.SMA(df['Close'], timeperiod=50)
    df['SMA_200'] = talib.SMA(df['Close'], timeperiod=200)
    
    # RSI (Relative Strength Index)
    df['RSI'] = talib.RSI(df['Close'], timeperiod=14)
    
    # MACD
    macd, macd_signal, macd_hist = talib.MACD(df['Close'])
    df['MACD'] = macd
    df['MACD_Signal'] = macd_signal
    df['MACD_Hist'] = macd_hist
    
    # Bollinger Bands
    upper, middle, lower = talib.BBANDS(df['Close'], timeperiod=20)
    df['BB_Upper'] = upper
    df['BB_Middle'] = middle
    df['BB_Lower'] = lower
    
    # Volume indicators
    df['Volume_MA20'] = talib.SMA(df['Volume'], timeperiod=20)
    
    return df

def plot_price_with_indicators(df, symbol):
    """Create a comprehensive plot with price and indicators."""
    plt.figure(figsize=(15, 20))
    
    # Price and Moving Averages
    plt.subplot(4, 1, 1)
    plt.plot(df.index, df['Close'], label='Close Price', alpha=0.7)
    plt.plot(df.index, df['SMA_20'], label='20-day SMA', alpha=0.7)
    plt.plot(df.index, df['SMA_50'], label='50-day SMA', alpha=0.7)
    plt.plot(df.index, df['SMA_200'], label='200-day SMA', alpha=0.7)
    plt.title(f'{symbol} Price and Moving Averages')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Volume
    plt.subplot(4, 1, 2)
    plt.bar(df.index, df['Volume'], label='Volume', alpha=0.3)
    plt.plot(df.index, df['Volume_MA20'], label='20-day Volume MA', color='red')
    plt.title('Trading Volume')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # RSI
    plt.subplot(4, 1, 3)
    plt.plot(df.index, df['RSI'], label='RSI (14)', color='purple')
    plt.axhline(70, color='red', linestyle='--', alpha=0.5)
    plt.axhline(30, color='green', linestyle='--', alpha=0.5)
    plt.ylim(0, 100)
    plt.title('Relative Strength Index (RSI)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # MACD
    plt.subplot(4, 1, 4)
    plt.plot(df.index, df['MACD'], label='MACD', color='blue')
    plt.plot(df.index, df['MACD_Signal'], label='Signal Line', color='red')
    plt.bar(df.index, df['MACD_Hist'] * 3, label='MACD Histogram', color='gray', alpha=0.3)
    plt.title('MACD')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Create output directory if it doesn't exist
    os.makedirs('../output', exist_ok=True)
    plt.savefig(f'../output/{symbol}_technical_analysis.png')
    plt.close()

def calculate_metrics(df):
    """Calculate financial metrics using PyNance."""
    # Calculate daily returns
    df['Daily_Return'] = df['Close'].pct_change() * 100
    
    # Calculate cumulative returns
    df['Cumulative_Return'] = (1 + df['Daily_Return']/100).cumprod() - 1
    
    # Calculate drawdowns
    df['Cumulative_Max'] = df['Close'].cummax()
    df['Drawdown'] = (df['Close'] - df['Cumulative_Max']) / df['Cumulative_Max'] * 100
    
    return df

def analyze_stock(symbol, start_date=None, end_date=None):
    """Main function to analyze a stock."""
    try:
        # Load data
        df = load_stock_data(symbol, start_date, end_date)
        
        # Add technical indicators
        df = add_technical_indicators(df)
        
        # Calculate financial metrics
        df = calculate_metrics(df)
        
        # Plot the data
        plot_price_with_indicators(df, symbol)
        
        # Print key metrics
        print(f"\n=== {symbol} Analysis ===")
        print(f"Analysis Period: {df.index[0].date()} to {df.index[-1].date()}")
        print(f"Total Return: {df['Cumulative_Return'].iloc[-1] * 100:.2f}%")
        print(f"Max Drawdown: {df['Drawdown'].min():.2f}%")
        print(f"Current RSI: {df['RSI'].iloc[-1]:.2f}")
        
        return df
        
    except Exception as e:
        print(f"Error analyzing {symbol}: {str(e)}")
        return None

if __name__ == "__main__":
    import sys
    
    # Default stock symbol is AAPL if none provided
    symbol = sys.argv[1] if len(sys.argv) > 1 else 'AAPL'
    
    # Analyze the stock
    df = analyze_stock(symbol)
    
    if df is not None:
        print(f"\nAnalysis complete! Results saved to 'output/{symbol}_technical_analysis.png'")
        print("\nFirst few rows of the analysis:")
        print(df[['Open', 'High', 'Low', 'Close', 'Volume', 'SMA_20', 'RSI']].tail())
