#!/usr/bin/env python3

import sys
print("Python version:", sys.version)

try:
    import pyspark
    print("PySpark version:", pyspark.__version__)
    
    from pyspark.sql import SparkSession
    print("PySpark imports successful")
    
    # Create a simple Spark session
    spark = SparkSession.builder.appName('PySpark Test').getOrCreate()
    print("Spark session created successfully")
    print("Spark version:", spark.version)
    
    # Create a simple DataFrame to test
    data = [("Alice", 25), ("Bob", 30), ("Charlie", 35)]
    columns = ["Name", "Age"]
    df = spark.createDataFrame(data, columns)
    print("Test DataFrame created:")
    df.show()
    
    spark.stop()
    print("PySpark test completed successfully!")
    
except ImportError as e:
    print("Error importing PySpark:", e)
except Exception as e:
    print("Error running PySpark:", e)
