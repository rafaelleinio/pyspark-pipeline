from pyspark.sql import DataFrame, functions
from pyspark.sql.types import IntegerType, StringType, StructField, StructType

import pyspark_pipeline as pp

SOURCE_SCHEMA = StructType(
    fields=[
        StructField(name="version", dataType=IntegerType(), nullable=False),
        StructField(
            name="record",
            dataType=StructType(
                fields=[
                    StructField(
                        name="field_group_one",
                        dataType=StructType(
                            fields=[
                                StructField(
                                    name="key1", dataType=StringType(), nullable=False
                                ),
                                StructField(
                                    name="key2", dataType=StringType(), nullable=False
                                ),
                                StructField(
                                    name="key3", dataType=StringType(), nullable=False
                                ),
                            ]
                        ),
                        nullable=False,
                    ),
                    StructField(
                        name="field_group_two",
                        dataType=StructType(
                            fields=[
                                StructField(
                                    name="days_since_event",
                                    dataType=IntegerType(),
                                    nullable=False,
                                ),
                                StructField(
                                    name="key4", dataType=StringType(), nullable=False
                                ),
                                StructField(
                                    name="key5", dataType=StringType(), nullable=False
                                ),
                            ]
                        ),
                        nullable=False,
                    ),
                ]
            ),
            nullable=False,
        ),
    ]
)


class SamplePipeline(pp.ETLPipeline):
    """Simple ETL reading from jsonl and writing to a SQL database."""

    def _extract(self) -> DataFrame:
        return pp.io.read_json_dataset(
            spark_client=self.spark_client,
            path="data/input/sample_dataset.jsonl",
            schema=SOURCE_SCHEMA,
        )

    def _transform(self, df: DataFrame) -> DataFrame:
        """Filter out events older than 3000 days."""
        return df.where(
            functions.expr("record.field_group_two.days_since_event < 3000")
        )

    def _load(self, df: DataFrame) -> None:
        db_df = df.withColumn(colName="record", col=functions.to_json("record"))
        pp.io.write_jdbc(df=db_df, table="sample_dataset")
