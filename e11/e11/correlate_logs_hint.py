import sys
assert sys.version_info >= (3, 8) # make sure we have Python 3.8+
from pyspark.sql import SparkSession, functions, types, Row
import re


line_re = re.compile(r"^(\S+) - - \[\S+ [+-]\d+\] \"[A-Z]+ \S+ HTTP/\d\.\d\" \d+ (\d+)$")


def line_to_row(line):
    """
    Take a logfile line and return a Row object with hostname and bytes transferred.
    Return None if regex doesn't match.
    """
    m = line_re.match(line)
    if m:
        return Row(hostname=m.group(1), bytes=int(m.group(2)))
    else:
        return None


def not_none(row):
    """
    Is this None? Hint: .filter() with it.
    """
    return row is not None


def create_row_rdd(in_directory):
    log_lines = spark.sparkContext.textFile(in_directory)
    # Return an RDD of Row() objects
    return log_lines.map(line_to_row).filter(not_none)


def main(in_directory):
    logs = spark.createDataFrame(create_row_rdd(in_directory))

    # Group by hostname to get request count and total bytes
    host_stats = logs.groupBy('hostname').agg(
        functions.count('*').alias('count'),
        functions.sum('bytes').alias('bytes')
    )
    
    # Calculate the six sums needed for correlation coefficient
    sums = host_stats.agg(
        functions.count('*').alias('n'),
        functions.sum('count').alias('sum_x'),
        functions.sum('bytes').alias('sum_y'),
        functions.sum(functions.col('count') * functions.col('bytes')).alias('sum_xy'),
        functions.sum(functions.col('count') * functions.col('count')).alias('sum_x2'),
        functions.sum(functions.col('bytes') * functions.col('bytes')).alias('sum_y2')
    ).first()
    
    # Extract the six values
    n = float(sums.n)
    sum_x = float(sums.sum_x)
    sum_y = float(sums.sum_y)
    sum_xy = float(sums.sum_xy)
    sum_x2 = float(sums.sum_x2)
    sum_y2 = float(sums.sum_y2)
    
    # Calculate correlation coefficient
    numerator = n * sum_xy - sum_x * sum_y
    denominator = ((n * sum_x2 - sum_x * sum_x) * (n * sum_y2 - sum_y * sum_y)) ** 0.5
    r = numerator / denominator

    print(f"r = {r}")
    print(f"r^2 = {r*r}")
    # Built-in function should get the same results.
    #print(host_stats.corr('count', 'bytes'))


if __name__=='__main__':
    in_directory = sys.argv[1]
    spark = SparkSession.builder.appName('correlate logs').getOrCreate()
    assert spark.version >= '3.2' # make sure we have Spark 3.2+
    spark.sparkContext.setLogLevel('WARN')

    main(in_directory)
