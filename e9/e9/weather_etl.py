import sys
from pyspark.sql import SparkSession, functions, types

spark = SparkSession.builder.appName('weather ETL').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 8) # make sure we have Python 3.8+
assert spark.version >= '3.2' # make sure we have Spark 3.2+

observation_schema = types.StructType([
    types.StructField('station', types.StringType()),
    types.StructField('date', types.StringType()),
    types.StructField('observation', types.StringType()),
    types.StructField('value', types.IntegerType()),
    types.StructField('mflag', types.StringType()),
    types.StructField('qflag', types.StringType()),
    types.StructField('sflag', types.StringType()),
    types.StructField('obstime', types.StringType()),
])


def main(in_directory, out_directory):
    # Read the CSV files with gzip compression
    weather = spark.read.csv(in_directory, schema=observation_schema)

    # Filter the data based on requirements:
    # 1. qflag (quality flag) is null
    # 2. station starts with 'CA'
    # 3. observation is 'TMAX'
    filtered_data = weather.filter(
        (weather.qflag.isNull()) &
        (weather.station.startswith('CA')) &
        (weather.observation == 'TMAX')
    )

    # Transform the data:
    # 1. Divide temperature by 10 to get °C and rename to 'tmax'
    # 2. Select only the columns we need: station, date, tmax
    cleaned_data = filtered_data.select(
        weather.station,
        weather.date,
        (weather.value / 10.0).alias('tmax')
    )

    # Write as JSON files with gzip compression
    cleaned_data.write.json(out_directory, compression='gzip', mode='overwrite')


if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)
