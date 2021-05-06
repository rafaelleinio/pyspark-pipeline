from typing import Any, Dict, List, Optional, Union

from pandas import DataFrame as PandasDataFrame
from pyspark.sql import DataFrame
from pyspark.sql.types import StructType

from pyspark_test.core.spark_client import SparkClient


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
        path=path, format="csv", schema=schema, options=options or {}  # type: ignore
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
