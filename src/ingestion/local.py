from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def read_csv_local(
    spark: SparkSession,
    source_path: str,
):
    return (
        spark.read
        .format("csv")
        .option("header", "true")
        .option("inferSchema", "true")
        .load(source_path)
    )


def write_bronze_local(
    df,
    target_path: str,
):
    (
        df
        .withColumn("_source_file", F.input_file_name())
        .withColumn("_ingestion_timestamp", F.current_timestamp())
        .write
        .format("delta")
        .mode("append")
        .save(target_path)
    )