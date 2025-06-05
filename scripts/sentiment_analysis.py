import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
import yfinance as yf
from datetime import datetime, timedelta
import os

class SentimentAnalyzer:
    def __init__(self):
        self.sentiment_scores = []
        
    def analyze_sentiment(self, text):
        """Basic sentiment analysis using TextBlob."""
        if not isinstance(text, str) or not text.strip():
            return 0.0
        return TextBlob(text).sentiment.polarity

    def analyze_news(self, news_file):
        """Analyze sentiment of news headlines."""
        # Load news data
        df = pd.read_csv(news_file)
        
        # Ensure we have required columns
        if 'headline' not in df.columns or 'date' not in df.columns:
            raise ValueError("CSV must contain 'headline' and 'date' columns")
        
        # Convert date column
        df['date'] = pd.to_datetime(df['date']).dt.normalize()
        
        # Calculate sentiment
        df['sentiment'] = df['headline'].apply(self.analyze_sentiment)
        
        # Group by date
        daily_sentiment = df.groupby('date')['sentiment'].mean().reset_index()
        
        return daily_sentiment

    def get_stock_data(self, symbol, start_date, end_date):
        """Get stock price data."""
        df = yf.download(symbol, start=start_date, end=end_date, progress=False)
        df['daily_return'] = df['Close'].pct_change() * 100
        return df

    def analyze_correlation(self, news_file, stock_symbol):
        """Analyze correlation between news sentiment and stock returns."""
        # Get news sentiment
        sentiment_df = self.analyze_news(news_file)
        
        # Get date range from news data
        start_date = sentiment_df['date'].min() - timedelta(days=1)
        end_date = sentiment_df['date'].max() + timedelta(days=1)
        
        # Get stock data
        stock_df = self.get_stock_data(stock_symbol, start_date, end_date)
        
        # Merge data
        merged = pd.merge(
            sentiment_df,
            stock_df[['Close', 'daily_return']],
            left_on='date',
            right_index=True,
            how='inner'
        )
        
        # Calculate correlation
        correlation = merged['sentiment'].corr(merged['daily_return'])
        
        # Create output directory
        os.makedirs('../output', exist_ok=True)
        
        # Plot results
        self._plot_results(merged, stock_symbol, correlation)
        
        return {
            'correlation': correlation,
            'data': merged
        }
    
    def _plot_results(self, data, symbol, correlation):
        """Create visualization of results."""
        plt.figure(figsize=(12, 8))
        
        # Plot 1: Price and Sentiment
        ax1 = plt.subplot(2, 1, 1)
        ax1.plot(data['date'], data['Close'], 'b-', label='Stock Price')
        ax1.set_ylabel('Price', color='b')
        ax1.tick_params(axis='y', labelcolor='b')
        
        ax2 = ax1.twinx()
        ax2.bar(data['date'], data['sentiment'], color='r', alpha=0.3, width=0.5, label='Sentiment')
        ax2.axhline(0, color='black', linestyle='--', alpha=0.5)
        ax2.set_ylabel('Sentiment', color='r')
        ax2.tick_params(axis='y', labelcolor='r')
        
        plt.title(f'{symbol} Stock Price vs News Sentiment')
        
        # Plot 2: Scatter plot
        plt.subplot(2, 1, 2)
        sns.regplot(x='sentiment', y='daily_return', data=data)
        plt.axhline(0, color='black', linestyle='--', alpha=0.5)
        plt.axvline(0, color='black', linestyle='--', alpha=0.5)
        plt.xlabel('Sentiment Score')
        plt.ylabel('Daily Return (%)')
        plt.title(f'Sentiment vs Returns (Correlation: {correlation:.2f})')
        
        plt.tight_layout()
        plt.savefig(f'../output/{symbol}_sentiment_analysis.png')
        plt.close()

if __name__ == "__main__":
    # Example usage
    analyzer = SentimentAnalyzer()
    results = analyzer.analyze_correlation(
        news_file='./data/raw_analyst_ratings.csv',
        stock_symbol='AAPL'
    )
    print(f"Correlation between news sentiment and stock returns: {results['correlation']:.2f}")
