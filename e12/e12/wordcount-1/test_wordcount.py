#!/usr/bin/env python3

"""
Test script for wordcount.py
This script extracts the compressed text files and runs the word count analysis.
"""

import os
import gzip
import shutil
import subprocess
import sys

def extract_gz_files():
    """Extract .gz files to create a text directory for processing"""
    text_dir = "text_files"
    if not os.path.exists(text_dir):
        os.makedirs(text_dir)
    
    gz_files = [f for f in os.listdir('.') if f.endswith('.txt.gz')]
    
    for gz_file in gz_files:
        txt_file = gz_file[:-3]  # Remove .gz extension
        txt_path = os.path.join(text_dir, txt_file)
        
        print(f"Extracting {gz_file} to {txt_path}")
        with gzip.open(gz_file, 'rt', encoding='utf-8') as f_in:
            with open(txt_path, 'w', encoding='utf-8') as f_out:
                shutil.copyfileobj(f_in, f_out)
    
    return text_dir

def run_wordcount(input_dir, output_dir):
    """Run the wordcount.py script"""
    cmd = [sys.executable, "wordcount.py", input_dir, output_dir]
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        print("STDOUT:")
        print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running wordcount: {e}")
        return False

def main():
    print("Word Count Test Script")
    print("=" * 40)
    
    # Extract compressed files
    print("Step 1: Extracting compressed text files...")
    input_dir = extract_gz_files()
    
    # Run word count
    output_dir = "wordcount_output"
    print(f"\nStep 2: Running word count analysis...")
    success = run_wordcount(input_dir, output_dir)
    
    if success:
        print(f"\nWord count completed successfully!")
        print(f"Results are in: {output_dir}")
        
        # Show output files
        if os.path.exists(output_dir):
            print("\nOutput files:")
            for file in os.listdir(output_dir):
                print(f"  - {file}")
    else:
        print("\nWord count failed!")

if __name__ == "__main__":
    main()
