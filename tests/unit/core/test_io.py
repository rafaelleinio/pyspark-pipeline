from unittest.mock import Mock, patch

from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType, StringType, StructField, StructType

from pyspark_pipeline.core import io


@patch("pyspark.sql.readwriter.DataFrameReader.load")
def test_read_csv_dataset(mock_load: Mock, spark_client):
    # act
    _ = io.read_csv_dataset(
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
        header=False,
    )


@patch("pandas.core.generic.NDFrame.to_csv")
def test_write_single_csv_dataset(mock_to_csv: Mock, spark_session: SparkSession):
    # arrange
    df = spark_session.sql("select 1 as id")

    # act
    io.write_single_csv_dataset(df=df, path="path/to/file", options={"header": True})

    # assert
    mock_to_csv.assert_called_with("path/to/file", index=False, header=True)


@patch("pyspark.sql.readwriter.DataFrameReader.load")
def test_read_json_dataset(mock_load: Mock, spark_client):
    schema = StructType(
        fields=[
            StructField(name="id", dataType=IntegerType(), nullable=True),
            StructField(
                name="struct_field",
                dataType=StructType(
                    fields=[
                        StructField(name="field1", dataType=StringType(), nullable=True)
                    ]
                ),
                nullable=True,
            ),
        ]
    )

    # act
    _ = io.read_json_dataset(
        spark_client,
        path="path/to/file.json",
        schema=schema,
    )

    # assert
    mock_load.assert_called_with(
        path="path/to/file.json",
        format="json",
        schema=schema,
    )


@patch("pyspark.sql.readwriter.DataFrameWriter.jdbc")
def test_write_jdbc(mock_write_jdbc: Mock, spark_session: SparkSession):
    # arrange
    df = spark_session.sql("select 1 as id")

    # act
    io.write_jdbc(df=df, table="table", mode="append")

    # assert
    mock_write_jdbc.assert_called_with(
        url="jdbc:sqlite://None:None/database.db",
        table="table",
        mode="append",
        properties={
            "user": "None",
            "password": "None",
            "driver": "org.postgresql.Driver",
            "stringtype": "unspecified",
        },
    )
