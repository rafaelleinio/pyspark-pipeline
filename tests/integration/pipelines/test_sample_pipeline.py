import pathlib
from unittest import mock

from pyspark.sql import DataFrame
from pyspark.sql.types import IntegerType, StringType, StructField, StructType

import pyspark_pipeline as pp

CURRENT_PATH = pathlib.Path(__file__).parent.resolve()


class TestSamplePipeline:
    @mock.patch("pyspark_pipeline.core.io.write_jdbc")
    def test_run(self, mock_write_jdbc: mock.Mock, spark_client):
        # arrange
        pipeline = pp.pipelines.SamplePipeline(spark_client=spark_client)

        target_df = pp.io.read_json_dataset(
            spark_client=spark_client,
            path=f"{CURRENT_PATH}/sample_pipeline_target.jsonl",
            schema=StructType(
                fields=[
                    StructField(name="version", dataType=IntegerType(), nullable=False),
                    StructField(name="record", dataType=StringType(), nullable=False),
                ]
            ),
        )

        # act
        pipeline.run()
        output_df: DataFrame = mock_write_jdbc.call_args.kwargs["df"]

        # assert
        pp.testing.assert_dataframe_equality(output_df=output_df, target_df=target_df)
