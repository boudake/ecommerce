from ingestion.autoloader import (
    read_csv_autoloader,
    write_bronze,
)

from ingestion.local import (
    read_csv_local,
    write_bronze_local,
)


def run(spark, config):

    dataset = config["datasets"]["orders"]

    environment = config["app"]["environment"]

    if environment == "local":

        df = read_csv_local(
            spark=spark,
            source_path=dataset["source"],
        )

        return write_bronze_local(
            df=df,
            target_path=dataset["target"],
        )

    elif environment == "databricks":

        df = read_csv_autoloader(
            spark=spark,
            source_path=dataset["source"],
            schema_location=dataset["schema_location"],
        )

        return write_bronze(
            df=df,
            target_table=dataset["target"],
            checkpoint_location=dataset["checkpoint_location"],
        )

    else:
        raise ValueError(
            f"Unsupported environment: {environment}"
        )