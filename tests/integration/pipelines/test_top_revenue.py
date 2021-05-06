from pyspark_test.core.io import read_csv_dataset
from pyspark_test.core.testing import assert_dataframe_equality
from pyspark_test.pipelines.top_revenue import TopRevenuePipeline


class TestTopRevenuePipeline:
    def test_run(self):
        # arrange
        pipeline = TopRevenuePipeline()
        schema = "year_month string, product_name string, total_revenue decimal(38, 2)"
        options = {"header": True}
        target_df = read_csv_dataset(
            spark_client=pipeline.spark_client,
            path="tests/integration/pipelines/target_data.csv",
            schema=schema,
            options=options,
        )

        # act
        pipeline.run()
        output_df = read_csv_dataset(
            spark_client=pipeline.spark_client,
            path="data/output/output.csv",
            schema=schema,
            options=options,
        )

        # assert
        assert_dataframe_equality(output_df=output_df, target_df=target_df)
