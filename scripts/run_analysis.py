# scripts/run_analysis.py
from text_analysis import analyze_text_data
from publisher_analysis import analyze_publishers
from time_series_analysis import analyze_time_series

def main():
    # Run text analysis
    print("Running text analysis...")
    df = analyze_text_data()
    
    # Run publisher analysis
    print("\nRunning publisher analysis...")
    analyze_publishers(df)
    
    # Run time series analysis
    print("\nRunning time series analysis...")
    analyze_time_series(df)
    
    print("\nAll analyses completed! Check the 'output' directory for results.")

if __name__ == "__main__":
    main()