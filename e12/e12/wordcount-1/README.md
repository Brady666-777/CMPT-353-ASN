# E12 Exercises: Word Count & Pup Inflation Analysis

This project contains implementations for two data analysis tasks:

1. Word Count analysis using Apache Spark DataFrames
2. Pup Inflation analysis of @dog_rates Twitter data

## Files

### Word Count Task

- `wordcount.py` - Main word count program using Spark DataFrames
- `test_wordcount.py` - Test script that extracts compressed files and runs the analysis
- `austen-persuasion.txt.gz` - Jane Austen's Persuasion
- `austen-sense.txt.gz` - Jane Austen's Sense and Sensibility
- `carroll-alice.txt.gz` - Lewis Carroll's Alice's Adventures in Wonderland

### Pup Inflation Task

- `pup_inflation_analysis.py` - Analysis script for @dog_rates Twitter data
- Creates `pup_inflation.pdf` - Blog post with visualizations

### Dependencies

- `requirements.txt` - Basic dependencies for word count
- `requirements_full.txt` - All dependencies for both tasks

## Requirements

- Python 3.x
- Apache Spark with PySpark (for word count)
- Java (required for Spark)
- Various Python data science libraries (see requirements files)

## Installation

Install all dependencies:

```bash
pip install -r requirements_full.txt
```

Or install just for word count:

```bash
pip install -r requirements.txt
```

## Task 1: Word Count

### Usage

#### Method 1: Direct usage

```bash
python wordcount.py <input_directory> <output_directory>
```

#### Method 2: Using the test script

```bash
python test_wordcount.py
```

The test script will:

1. Extract the compressed text files to a `text_files` directory
2. Run the word count analysis
3. Save results to `wordcount_output` directory

### Output

The program outputs CSV files with:

- Column 1: Word (lowercase)
- Column 2: Count

Results are sorted by:

1. Count (descending - most frequent first)
2. Alphabetically (for ties)

Empty strings are filtered out from the results.

### Implementation Details

The program uses Spark DataFrames to:

1. Read text files using `spark.read.text()`
2. Split lines into words using regex pattern for punctuation and spaces
3. Convert all words to lowercase using `lower()`
4. Use `explode()` to create separate rows for each word
5. Filter out empty strings
6. Group by word and count occurrences
7. Sort by count (descending) and word (ascending)
8. Write results as uncompressed CSV

The word-breaking regex pattern matches spaces and/or punctuation:

```python
wordbreak = r'[%s\s]+' % (re.escape(string.punctuation),)
```

## Task 2: Pup Inflation Analysis

### Usage

```bash
python pup_inflation_analysis.py
```

This script will:

1. Load dog ratings data (currently uses sample data)
2. Create two main visualizations:
   - Scatter plot with trend line showing ratings over time
   - Box plots showing rating distribution by year
3. Generate a PDF report (`pup_inflation.pdf`) with analysis

### Data Requirements

The script currently uses sample data for demonstration. To use with real data:

1. Replace the `load_data()` function to load your actual @dog_rates dataset
2. Ensure the data has columns: `date`, `rating`, `tweet_text`

### Output

- Interactive plots displayed during execution
- `pup_inflation.pdf` - Complete blog post with visualizations and analysis

### Analysis Features

- Statistical trend analysis with linear regression
- R² and p-value calculations
- Distribution analysis over time
- Professional blog post format suitable for general audience

## Expected Results

### Word Count

You should find that common English words like "the", "to", "and", "of" are the most frequent across the Jane Austen and Lewis Carroll texts.

### Pup Inflation

The analysis demonstrates the "pup inflation" phenomenon where @dog_rates scores have increased over time, with statistical evidence and compelling visualizations.
