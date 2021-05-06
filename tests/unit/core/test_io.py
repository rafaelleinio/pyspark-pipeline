from unittest.mock import Mock, patch

from pyspark.sql import SparkSession

from pyspark_test.core.io import read_csv_dataset, write_single_csv_dataset
from pyspark_test.core.spark_client import SparkClient


@patch("pyspark.sql.readwriter.DataFrameReader.load")
def test_read_csv_dataset(mock_load: Mock):
    # arrange
    spark_client = SparkClient()
    spark_client.create_session()

    # act
    _ = read_csv_dataset(
        spark_client,
        path="path/to/file",
        schema="id int, name string",
        options={"header": False},
    )

    # assert
    mock_load.assert_called_with(
        path="path/to/file",
        format="csv",
        schema="id int, name string",
        options={"header": False},
    )


@patch("pandas.core.generic.NDFrame.to_csv")
def test_write_single_csv_dataset(mock_to_csv: Mock, spark_session: SparkSession):
    # arrange
    df = spark_session.sql("select 1 as id")

    # act
    write_single_csv_dataset(df=df, path="path/to/file", options={"header": True})

    # assert
    mock_to_csv.assert_called_with("path/to/file", index=False, header=True)
