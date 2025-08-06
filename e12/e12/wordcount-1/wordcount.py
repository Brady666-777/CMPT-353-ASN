#!/usr/bin/env python3

import sys
import string
import re
from pyspark.sql import SparkSession
from pyspark.sql.functions import split, explode, lower, col, count, desc

def main():
    if len(sys.argv) != 3:
        print("Usage: python wordcount.py <input_directory> <output_directory>")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    
    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("WordCount") \
        .getOrCreate()
    
    try:
        # Read all text files from input directory
        df = spark.read.text(input_dir)
        
        # Define word break regex pattern (spaces and/or punctuation)
        wordbreak = r'[%s\s]+' % (re.escape(string.punctuation),)
        
        # Split lines into words, explode into separate rows, and convert to lowercase
        words_df = df.select(
            explode(split(lower(col("value")), wordbreak)).alias("word")
        )
        
        # Filter out empty strings
        words_df = words_df.filter(col("word") != "")
        
        # Count occurrences of each word
        word_counts = words_df.groupBy("word").agg(count("*").alias("count"))
        
        # Sort by count (descending) and then alphabetically by word
        sorted_counts = word_counts.orderBy(desc("count"), "word")
        
        # Write results as CSV (uncompressed)
        sorted_counts.coalesce(1).write \
            .mode("overwrite") \
            .option("header", "false") \
            .csv(output_dir)
        
        print(f"Word count completed. Results written to {output_dir}")
        
        # Show top 10 words for verification
        print("\nTop 10 most frequent words:")
        sorted_counts.show(10)
        
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
