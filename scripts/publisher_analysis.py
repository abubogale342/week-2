# scripts/publisher_analysis.py
from utils import load_data, setup_environment
import matplotlib.pyplot as plt

def analyze_publishers(df, top_n=10):
    """Analyze and plot publisher statistics."""
    if 'publisher' not in df.columns:
        print("No publisher column found in the dataset.")
        return
    
    publisher_counts = df['publisher'].value_counts()
    
    print("\n=== Publisher Statistics ===")
    print(f"Total unique publishers: {len(publisher_counts)}")
    print("\nTop publishers by article count:")
    print(publisher_counts.head(top_n))
    
    # Plot top publishers
    plt.figure(figsize=(12, 6))
    publisher_counts.head(top_n).plot(kind='bar')
    plt.title(f'Top {top_n} Publishers by Number of Articles')
    plt.xlabel('Publisher')
    plt.ylabel('Number of Articles')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('../output/publisher_distribution.png')
    plt.close()

if __name__ == "__main__":
    import os
    setup_environment()
    data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                           'data', 'raw_analyst_ratings.csv')
    df = load_data(data_path)
    analyze_publishers(df)