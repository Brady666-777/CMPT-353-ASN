#!/usr/bin/env python3

"""
Pup Inflation Analysis
Analysis of @dog_rates Twitter account ratings over time

This script creates visualizations and analysis for the pup inflation blog post.
Note: This requires the dog ratings dataset from previous exercises.
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.patches as mpatches
from datetime import datetime

# Set seaborn style for nicer plots
sns.set_style("whitegrid")
sns.set_palette("husl")

def load_data():
    """
    Load the dog ratings dataset from Exercise 2
    """
    import os
    import re
    
    # Path to the real data from Exercise 2
    data_path = r'c:\Users\wohai\Documents\e2\e2\dog_rates_tweets.csv'
    
    print("Loading dog ratings data...")
    print(f"Loading data from: {os.path.abspath(data_path)}")
    
    # Load the CSV file
    df = pd.read_csv(data_path)
    print(f"Loaded {len(df)} total tweets")
    
    # Extract ratings from text using regex (similar to Exercise 2/7)
    def extract_rating(text):
        if pd.isna(text):
            return None
        # Look for patterns like "13/10", "12.5/10", etc.
        pattern = r'(\d+(?:\.\d+)?)/10'
        matches = re.findall(pattern, text)
        if matches:
            try:
                return float(matches[-1])  # Take the last match
            except ValueError:
                return None
        return None
    
    # Extract ratings
    df['rating'] = df['text'].apply(extract_rating)
    
    # Filter to only tweets with ratings
    df_rated = df[df['rating'].notna()].copy()
    print(f"Found {len(df_rated)} tweets with ratings")
    
    # Convert timestamp to datetime
    df_rated['date'] = pd.to_datetime(df_rated['created_at'])
    
    # Clean up extreme outliers (keep reasonable ratings)
    df_rated = df_rated[(df_rated['rating'] >= 0) & (df_rated['rating'] <= 20)].copy()
    
    print(f"Loaded {len(df_rated)} rated tweets")
    print(f"Date range: {df_rated['date'].min().date()} to {df_rated['date'].max().date()}")
    print(f"Rating range: {df_rated['rating'].min()} to {df_rated['rating'].max()}")
    print(f"Mean rating: {df_rated['rating'].mean():.2f}")
    print(f"Median rating: {df_rated['rating'].median()}")
    
    # Show early vs recent comparison
    cutoff_date = pd.to_datetime('2017-01-01')
    early = df_rated[df_rated['date'] < cutoff_date]['rating']
    recent = df_rated[df_rated['date'] >= cutoff_date]['rating']
    
    if len(early) > 0 and len(recent) > 0:
        print(f"Early period (before 2017): Mean rating = {early.mean():.2f}")
        print(f"Recent period (2017+): Mean rating = {recent.mean():.2f}")
        print(f"Difference: {recent.mean() - early.mean():.2f} points")
    
    return df_rated

def create_scatter_plot_with_trend(df):
    """Create scatter plot with trend line"""
    plt.figure(figsize=(12, 8))
    
    # Convert date to numeric for regression
    df['date_numeric'] = pd.to_datetime(df['date']).astype('int64') / 10**9 / 86400  # days since epoch
    
    # Perform linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(df['date_numeric'], df['rating'])
    
    # Create scatter plot
    plt.scatter(df['date'], df['rating'], alpha=0.6, s=20, color='lightblue', label='Individual Ratings')
    
    # Add trend line
    trend_y = slope * df['date_numeric'] + intercept
    plt.plot(df['date'], trend_y, 'r-', linewidth=2, label=f'Trend Line (slope: {slope:.3f})')
    
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Rating (out of 10)', fontsize=12)
    plt.title('Dog Ratings Over Time: Evidence of "Pup Inflation"', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Add statistics text
    plt.text(0.02, 0.98, f'R² = {r_value**2:.4f}\np-value = {p_value:.2e}', 
             transform=plt.gca().transAxes, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    return plt.gcf()

def create_rating_distribution_over_time(df):
    """Create visualization showing rating distribution changes over time"""
    plt.figure(figsize=(12, 8))
    
    # Group data by year
    df['year'] = pd.to_datetime(df['date']).dt.year
    years = sorted(df['year'].unique())
    
    # Create box plots for each year
    data_by_year = [df[df['year'] == year]['rating'].values for year in years]
    
    box_plot = plt.boxplot(data_by_year, positions=years, widths=0.6, patch_artist=True)
    
    # Color the boxes with a gradient
    colors = plt.cm.viridis(np.linspace(0, 1, len(years)))
    for patch, color in zip(box_plot['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Rating (out of 10)', fontsize=12)
    plt.title('Distribution of Dog Ratings by Year', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    # Add median trend line
    medians = [np.median(data) for data in data_by_year]
    plt.plot(years, medians, 'ro-', linewidth=2, markersize=6, label='Median Rating')
    plt.legend()
    
    plt.tight_layout()
    return plt.gcf()

def generate_analysis_text():
    """Generate the blog post text content"""
    text = """
# Explaining Pup Inflation: A Data-Driven Look at @dog_rates

## The Phenomenon

If you've been following the @dog_rates Twitter account over the years, you might have noticed something interesting: dogs seem to be getting better ratings. What started as a quirky account rating dogs "out of 10" has evolved into something that consistently gives ratings well above 10. This phenomenon, which we're calling "pup inflation," appears to show a statistically significant upward trend in ratings over time.

## The Data Story

Our analysis of thousands of @dog_rates tweets reveals a clear pattern: ratings have been steadily increasing since the account's inception. The scatter plot below shows individual ratings plotted over time, with a clear upward trend line. The statistical evidence is compelling - we found a significant positive correlation between time and rating scores.

## What's Driving the Inflation?

Several factors might explain this upward trend:

1. **Audience Engagement**: As the account grew more popular, higher ratings might generate more engagement (likes, retweets, comments).

2. **Content Evolution**: The account may have shifted toward featuring objectively "better" dogs - perhaps more photogenic breeds or dogs in particularly endearing situations.

3. **Rating Scale Drift**: Like grade inflation in academia, the creator might have unconsciously adjusted their rating standards over time.

4. **Community Feedback**: Positive community response to higher ratings may have reinforced the behavior.

## The Numbers Don't Lie

The box plot visualization shows how the distribution of ratings has shifted over the years. Early years show ratings clustered around the expected 10/10 mark, while recent years show distributions centered well above 10, with some ratings reaching 14/10 or even higher.

This isn't just random variation - our statistical analysis shows the trend is highly significant, meaning it's extremely unlikely to have occurred by chance alone.

## Why This Matters

While this analysis might seem lighthearted, it illustrates important concepts about data drift and rating scale reliability. In more serious contexts, understanding how rating systems evolve over time is crucial for maintaining fair and consistent evaluations.

The @dog_rates phenomenon also demonstrates how social media dynamics can influence content creation in subtle but measurable ways. As creators respond to audience feedback, their content naturally evolves - even something as simple as dog ratings isn't immune to these forces.

## Conclusion

"Pup inflation" is real, and it's spectacular. While all dogs are indeed good dogs deserving of high ratings, the systematic increase in scores over time reveals fascinating insights about social media, audience engagement, and the evolution of online content.

The next time you see a 13/10 rating, remember: you're not just seeing a good dog, you're witnessing the result of years of social media evolution in action.
"""
    return text

def create_pdf_report(df, output_filename='pup_inflation.pdf'):
    """Create a PDF report with visualizations and text"""
    
    with PdfPages(output_filename) as pdf:
        # Create visualizations
        fig1 = create_scatter_plot_with_trend(df)
        pdf.savefig(fig1, bbox_inches='tight')
        plt.close(fig1)
        
        fig2 = create_rating_distribution_over_time(df)
        pdf.savefig(fig2, bbox_inches='tight')
        plt.close(fig2)
        
        # Add text content as a separate page
        fig_text = plt.figure(figsize=(8.5, 11))
        plt.axis('off')
        
        # Add the analysis text
        analysis_text = generate_analysis_text()
        plt.text(0.05, 0.95, analysis_text, transform=fig_text.transFigure, 
                fontsize=10, verticalalignment='top', wrap=True,
                bbox=dict(boxstyle='round,pad=1', facecolor='white', alpha=0.8))
        
        pdf.savefig(fig_text, bbox_inches='tight')
        plt.close(fig_text)
    
    print(f"PDF report saved as {output_filename}")

def main():
    """Main analysis function"""
    print("Pup Inflation Analysis")
    print("=" * 40)
    
    # Load data
    print("Loading data...")
    df = load_data()
    
    print(f"Loaded {len(df)} records")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"Rating range: {df['rating'].min():.2f} to {df['rating'].max():.2f}")
    print(f"Mean rating: {df['rating'].mean():.2f}")
    
    # Create visualizations
    print("\nCreating visualizations...")
    
    # Show plots interactively
    print("Creating scatter plot with trend...")
    create_scatter_plot_with_trend(df)
    plt.savefig('scatter_plot_trend.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print("Creating rating distribution plot...")
    create_rating_distribution_over_time(df)
    plt.savefig('rating_distribution.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # Create PDF report
    print("\nGenerating PDF report...")
    create_pdf_report(df)
    
    print("Analysis complete!")

if __name__ == "__main__":
    main()
