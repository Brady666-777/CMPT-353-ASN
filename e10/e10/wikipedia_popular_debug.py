import sys
import re
from pyspark.sql import SparkSession, functions, types

spark = SparkSession.builder.appName('wikipedia popular debug').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 8) # make sure we have Python 3.8+
assert spark.version >= '3.2' # make sure we have Spark 3.2+


# Schema for the pagecounts files
pagecounts_schema = types.StructType([
    types.StructField('language', types.StringType()),
    types.StructField('title', types.StringType()),
    types.StructField('views', types.LongType()),
    types.StructField('bytes', types.LongType()),
])


def filename_to_hour(filename):
    """
    Extract hour from filename like pagecounts-20160801-120000.gz
    Returns format: 20160801-12
    """
    # Use regex to extract the date-hour pattern from filename
    # Handle various path formats (file://, hdfs://, etc.)
    match = re.search(r'pagecounts-(\d{8})-(\d{2})\d{4}', filename)
    if match:
        date_part = match.group(1)  # YYYYMMDD
        hour_part = match.group(2)  # HH
        return f"{date_part}-{hour_part}"
    return None


def main(in_directory, out_directory):
    # Create UDF for filename to hour conversion
    path_to_hour = functions.udf(filename_to_hour, returnType=types.StringType())
    
    # Read the pagecounts files
    print("Reading pagecounts files...")
    pagecounts = spark.read.csv(in_directory, schema=pagecounts_schema, sep=' ') \
        .withColumn('filename', functions.input_file_name()) \
        .withColumn('hour', path_to_hour(functions.col('filename')))
    
    print("Data count:", pagecounts.count())
    print("Sample data:")
    pagecounts.show(5)
    
    # Filter for English Wikipedia pages only
    # Exclude Main_Page and Special: pages
    english_pages = pagecounts.filter(
        (functions.col('language') == 'en') &
        (functions.col('title') != 'Main_Page') &
        (~functions.col('title').startswith('Special:'))
    )
    
    print("English pages count:", english_pages.count())
    print("English pages sample:")
    english_pages.show(5)
    
    # Find the maximum views for each hour
    max_views_per_hour = english_pages.groupBy('hour').agg(
        functions.max('views').alias('max_views')
    )
    
    print("Max views per hour:")
    max_views_per_hour.show()
    
    # Join back to get the pages that have the maximum views for each hour
    most_popular = english_pages.join(
        max_views_per_hour,
        (english_pages.hour == max_views_per_hour.hour) &
        (english_pages.views == max_views_per_hour.max_views)
    ).select(
        english_pages.hour,
        english_pages.title,
        english_pages.views
    )
    
    print("Most popular pages:")
    most_popular.show()
    
    # Sort by hour and title (for ties)
    result = most_popular.sort('hour', 'title')
    
    print("Final result:")
    result.show()
    
    # Write the results as CSV
    result.write.csv(out_directory, mode='overwrite')
    print("Output written to:", out_directory)


if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)
