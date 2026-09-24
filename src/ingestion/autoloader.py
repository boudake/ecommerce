from pyspark.sql import functions as F


def ingest_csv_to_bronze(
    spark,
    source_path,
    target_table,
    schema_location,
    checkpoint_location
):

    df = (
        spark.readStream
        .format("cloudFiles")
        .option("cloudFiles.format", "csv")
        .option("cloudFiles.inferColumnTypes", "true")
        .option("cloudFiles.schemaLocation", schema_location)
        .option("header", "true")
        .load(source_path)
    )

    df = (
        df
        .withColumn("_source_file", F.input_file_name())
        .withColumn("_ingestion_timestamp", F.current_timestamp())
    )

    (
        df.writeStream
        .format("delta")
        .option("checkpointLocation", checkpoint_location)
        .outputMode("append")
        .trigger(availableNow=True)
        .toTable(target_table)
    )