from typing import Any, Dict, List, Optional, Union

from pandas import DataFrame as PandasDataFrame
from pyspark.sql import DataFrame
from pyspark.sql.types import StructType
from sqlalchemy.engine import URL, make_url

from pyspark_pipeline.core.env import get_database_url
from pyspark_pipeline.core.spark_client import SparkClient


def read_csv_dataset(
    spark_client: SparkClient,
    path: str,
    schema: Union[str, StructType],
    options: Optional[Dict[str, Any]] = None,
) -> DataFrame:
    """Get a dataframe from a csv dataset.

    Args:
        spark_client: client to use to connect to Spark session.
        path: path to file.
        schema: expected schema for the dataset.
        options: extra options to be passed to Spark's DataframeReader.

    Returns:
        Spark dataframe with data.

    """
    return spark_client.session.read.load(
        path=path, format="csv", schema=schema, **(options or {})
    )


def write_single_csv_dataset(
    df: DataFrame,
    path: str,
    order_by: Optional[List[str]] = None,
    options: Optional[Dict[str, Any]] = None,
) -> None:
    """Write a Dataframe to a single named CSV file.

    Caution: this function should be use just for small datasets, since it's not a
    distributed operation.

    Args:
        df: dataframe to be written.
        path: path to write the file.
        order_by: columns to order the single coalesced partition.
        options: extra options to be passed to Pandas to_csv method.

    """
    coalesced_df = df.coalesce(numPartitions=1)
    pdf: PandasDataFrame = (
        coalesced_df.orderBy(*order_by, ascending=True).toPandas()
        if order_by
        else coalesced_df.toPandas()
    )
    pdf.to_csv(path, index=False, **options)


def read_json_dataset(
    spark_client: SparkClient, path: str, schema: StructType
) -> DataFrame:
    """Get a dataframe from a json dataset.

    Args:
        spark_client: client to use to connect to Spark session.
        path: path to json file/folder.
        schema: expected structured schema for the json.

    Returns:
        Spark dataframe with data.

    """
    return spark_client.session.read.load(path=path, format="json", schema=schema)


def write_jdbc(
    df: DataFrame, table: str, mode: str = "append", url: str = get_database_url()
) -> None:
    """Write dataframe to a database using a jdbc connection.

    Args:
        df: data to write.
        table: table name in target database.
        mode: 'append' or 'overwrite' load modes.
        url: connection string to use in jdbc connection.
            Default to `get_database_url` service.

    """
    structured_url: URL = make_url(url)
    jdbc_url = (
        f"jdbc:{structured_url.get_backend_name()}://{structured_url.host}:"
        f"{structured_url.port}/{structured_url.database}"
    )
    df.write.jdbc(
        url=jdbc_url,
        table=table,
        mode=mode,
        properties={
            "user": str(structured_url.username),
            "password": str(structured_url.password),
            "driver": "org.postgresql.Driver",
            "stringtype": "unspecified",
        },
    )
