# scripts/text_analysis.py
from utils import load_data, setup_environment
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_text_lengths(df, text_column, output_prefix):
    """Analyze and plot text length distributions."""
    length_col = f"{text_column}_length"
    df[length_col] = df[text_column].str.len()
    
    # Print statistics
    print(f"\n{text_column.capitalize()} Length Statistics:")
    print(df[length_col].describe())
    
    # Plot distribution
    plt.figure(figsize=(10, 5))
    sns.histplot(df[length_col], bins=30, kde=True)
    plt.title(f'Distribution of {text_column.capitalize()} Lengths')
    plt.xlabel(f'{text_column.capitalize()} Length (characters)')
    plt.tight_layout()
    plt.savefig(f'./output/{output_prefix}_lengths.png')
    plt.close()

def analyze_text_data(data_path=None):
    """Main function to analyze text data.
    
    Args:
        data_path (str, optional): Path to the data file. If None, will look in ../data/raw_analyst_ratings.csv
    """
    setup_environment()
    if data_path is None:
        import os
        data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                               'data', 'raw_analyst_ratings.csv')
    df = load_data(data_path)
    
    if 'headline' in df.columns:
        analyze_text_lengths(df, 'headline', 'headline')
    
    if 'content' in df.columns:
        analyze_text_lengths(df, 'content', 'content')
    
    return df

if __name__ == "__main__":
    analyze_text_data()