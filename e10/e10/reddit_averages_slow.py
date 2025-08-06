import sys
from pyspark.sql import SparkSession, functions, types

spark = SparkSession.builder.appName('reddit averages').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 8) # make sure we have Python 3.8+
assert spark.version >= '3.2' # make sure we have Spark 3.2+


def main(in_directory, out_directory):
    # Read JSON without schema (slower)
    comments = spark.read.json(in_directory)

    # Calculate averages by subreddit without caching
    averages = comments.groupBy('subreddit').agg(
        functions.avg('score').alias('average_score')
    )

    # Sort by subreddit name and write to output
    averages_by_subreddit = averages.sort('subreddit')
    averages_by_subreddit.write.csv(out_directory + '-subreddit', mode='overwrite')

    # Sort by average score (highest first) and write to output
    # This will recalculate everything since we didn't cache
    averages_by_score = averages.sort(functions.desc('average_score'))
    averages_by_score.write.csv(out_directory + '-score', mode='overwrite')


if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)
