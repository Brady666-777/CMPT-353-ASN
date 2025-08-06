import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys

def create_plots(file1, file2):
    # Read the first file
    filename1 = pd.read_csv(file1, sep=' ', header=None, index_col=1, names=['lang', 'page', 'views', 'bytes'])
    
    # Read the second file
    filename2 = pd.read_csv(file2, sep=' ', header=None, index_col=1, names=['lang', 'page', 'views', 'bytes'])
    
    # Create the first plot: Distribution of Views
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    filename1_sorted = filename1.sort_values(by='views', ascending=False)
    plt.plot(filename1_sorted['views'].values)
    plt.title('Popularity Distribution')
    plt.xlabel('Rank')
    plt.ylabel('Views')
    
    # Create the second plot: Hourly Views
    plt.subplot(1, 2, 2)
    merged_data = pd.merge(filename1[['views']], filename2[['views']], left_index=True, right_index=True, suffixes=('_hour1', '_hour2'))
    plt.scatter(merged_data['views_hour1'], merged_data['views_hour2'])
    plt.xscale('log')
    plt.yscale('log')
    plt.title('Hourly Correlation')
    plt.xlabel('Views in Hour 1')
    plt.ylabel('Views in Hour 2')
    
    # Save the figure
    plt.savefig('wikipedia.png')
    print("Saved wikipedia.png")

# Main execution code to handle command line arguments
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python create_plots.py <file1> <file2>")
        sys.exit(1)
    
    create_plots(sys.argv[1], sys.argv[2])