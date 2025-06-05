# scripts/time_series_analysis.py
from utils import load_data, setup_environment
import matplotlib.pyplot as plt
import pandas as pd

def analyze_time_series(df, date_column='date'):
    """Analyze and plot time series data."""
    if date_column not in df.columns:
        print(f"No '{date_column}' column found in the dataset.")
        return
    
    # Convert to datetime with flexible parsing and sort
    df[date_column] = pd.to_datetime(df[date_column], format='mixed', errors='coerce')
    
    # Drop rows where date parsing failed
    if df[date_column].isna().any():
        print(f"Warning: {df[date_column].isna().sum()} rows had invalid dates and were dropped")
        df = df.dropna(subset=[date_column])
    
    df = df.sort_values(date_column)
    
    # Resample by day
    daily_counts = df.set_index(date_column).resample('D').size()
    
    # Plot time series
    plt.figure(figsize=(14, 6))
    daily_counts.plot()
    plt.title('Number of Articles Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Articles')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('../output/articles_over_time.png')
    plt.close()
    
    # Analyze weekly pattern
    df['day_of_week'] = df[date_column].dt.day_name()
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekly_avg = df['day_of_week'].value_counts().reindex(day_order)
    
    plt.figure(figsize=(10, 5))
    weekly_avg.plot(kind='bar')
    plt.title('Number of Articles by Day of Week')
    plt.xlabel('Day of Week')
    plt.ylabel('Number of Articles')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('../output/weekly_pattern.png')
    plt.close()

if __name__ == "__main__":
    import os
    setup_environment()
    data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                           'data', 'raw_analyst_ratings.csv')
    df = load_data(data_path)
    analyze_time_series(df)