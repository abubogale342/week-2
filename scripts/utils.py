# scripts/utils.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def setup_environment():
    """Set up the environment with common settings."""
    # Use a built-in matplotlib style that's similar to seaborn
    plt.style.use('ggplot')
    # Set seaborn style and color palette
    sns.set_theme(style="whitegrid")
    sns.set_palette("husl")
    # Create output directory if it doesn't exist
    os.makedirs('../output', exist_ok=True)

def load_data(filepath):
    """Load and return the dataset."""
    return pd.read_csv(filepath)