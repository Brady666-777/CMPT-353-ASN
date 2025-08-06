#!/usr/bin/env python3

"""
E12 Exercise Runner
This script demonstrates how to run both tasks for the E12 assignment.
"""

import os
import subprocess
import sys

def run_command(cmd, description):
    """Run a command and display the result"""
    print(f"\n{'='*60}")
    print(f"RUNNING: {description}")
    print(f"COMMAND: {' '.join(cmd)}")
    print('='*60)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
        
        if result.stdout:
            print("OUTPUT:")
            print(result.stdout)
        
        if result.stderr:
            print("WARNINGS/ERRORS:")
            print(result.stderr)
            
        if result.returncode == 0:
            print(f"✓ {description} completed successfully!")
        else:
            print(f"✗ {description} failed with return code {result.returncode}")
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"✗ Error running {description}: {e}")
        return False

def main():
    print("E12 Assignment - Task Runner")
    print("="*60)
    print("This script will run both tasks:")
    print("1. Word Count Analysis (Spark DataFrames)")
    print("2. Pup Inflation Analysis (@dog_rates)")
    print()
    
    # Task 1: Word Count
    print("TASK 1: WORD COUNT ANALYSIS")
    success1 = run_command([sys.executable, "test_wordcount.py"], "Word Count Analysis")
    
    if success1:
        print("\nWord count results summary:")
        # Try to show a few lines of results
        try:
            import glob
            csv_files = glob.glob("wordcount_output/*.csv")
            if csv_files and not csv_files[0].endswith('.crc'):
                with open(csv_files[0], 'r') as f:
                    lines = f.readlines()[:10]
                    print("Top 10 most frequent words:")
                    for i, line in enumerate(lines, 1):
                        word, count = line.strip().split(',')
                        print(f"  {i:2}. {word:<10} ({count} occurrences)")
        except Exception as e:
            print(f"Could not display results: {e}")
    
    # Task 2: Pup Inflation Analysis
    print("\n\nTASK 2: PUP INFLATION ANALYSIS")
    success2 = run_command([sys.executable, "pup_inflation_analysis.py"], "Pup Inflation Analysis")
    
    if success2:
        print("\nGenerated files:")
        files = ['pup_inflation.pdf', 'scatter_plot_trend.png', 'rating_distribution.png']
        for file in files:
            if os.path.exists(file):
                size = os.path.getsize(file)
                print(f"  ✓ {file} ({size:,} bytes)")
            else:
                print(f"  ✗ {file} (not found)")
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Task 1 (Word Count): {'✓ SUCCESS' if success1 else '✗ FAILED'}")
    print(f"Task 2 (Pup Inflation): {'✓ SUCCESS' if success2 else '✗ FAILED'}")
    
    if success1 and success2:
        print("\n🎉 All tasks completed successfully!")
        print("\nDeliverables:")
        print("- wordcount.py: Spark DataFrame word count program")
        print("- Word count CSV results in wordcount_output/")
        print("- pup_inflation.pdf: Blog post with analysis and visualizations")
    else:
        print("\n⚠️  Some tasks failed. Check the output above for details.")
    
    print("\nFor detailed usage instructions, see README.md")

if __name__ == "__main__":
    main()
