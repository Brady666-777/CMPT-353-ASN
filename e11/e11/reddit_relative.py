import sys
assert sys.version_info >= (3, 8) # make sure we have Python 3.8+
from pyspark.sql import SparkSession, functions, types

comments_schema = types.StructType([
    types.StructField('archived', types.BooleanType()),
    types.StructField('author', types.StringType()),
    types.StructField('author_flair_css_class', types.StringType()),
    types.StructField('author_flair_text', types.StringType()),
    types.StructField('body', types.StringType()),
    types.StructField('controversiality', types.LongType()),
    types.StructField('created_utc', types.StringType()),
    types.StructField('distinguished', types.StringType()),
    types.StructField('downs', types.LongType()),
    types.StructField('edited', types.StringType()),
    types.StructField('gilded', types.LongType()),
    types.StructField('id', types.StringType()),
    types.StructField('link_id', types.StringType()),
    types.StructField('name', types.StringType()),
    types.StructField('parent_id', types.StringType()),
    types.StructField('retrieved_on', types.LongType()),
    types.StructField('score', types.LongType()),
    types.StructField('score_hidden', types.BooleanType()),
    types.StructField('subreddit', types.StringType()),
    types.StructField('subreddit_id', types.StringType()),
    types.StructField('ups', types.LongType()),
    #types.StructField('year', types.IntegerType()),
    #types.StructField('month', types.IntegerType()),
])


def main(in_directory, out_directory):
    comments = spark.read.json(in_directory, schema=comments_schema)

    # Calculate average score for each subreddit
    averages = comments.groupBy('subreddit').agg(functions.avg('score').alias('avg_score'))
    
    # Exclude subreddits with average score <= 0
    averages = averages.filter(averages.avg_score > 0).cache()
    
    # Join comments with averages to calculate relative scores
    comments_with_avg = comments.join(averages.hint('broadcast'), 'subreddit')
    comments_with_rel = comments_with_avg.withColumn('rel_score', 
                                                    comments_with_avg.score / comments_with_avg.avg_score)
    
    # Find maximum relative score for each subreddit
    max_rel_scores = comments_with_rel.groupBy('subreddit').agg(functions.max('rel_score').alias('max_rel_score')).cache()
    
    # Join to get the best comments (authors) for each subreddit
    best_comments = comments_with_rel.join(max_rel_scores.hint('broadcast'), 'subreddit')
    best_author = best_comments.filter(best_comments.rel_score == best_comments.max_rel_score) \
                              .select('subreddit', 'author', 'rel_score')

    best_author.write.json(out_directory, mode='overwrite')


if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    spark = SparkSession.builder.appName('Reddit Relative Scores').getOrCreate()
    assert spark.version >= '3.2' # make sure we have Spark 3.2+
    spark.sparkContext.setLogLevel('WARN')

    main(in_directory, out_directory)
