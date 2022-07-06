import pyspark_pipeline as pp


class TestTopRevenuePipeline:
    def test_run(self, spark_client):
        # arrange
        pipeline = pp.pipelines.TopRevenuePipeline(spark_client=spark_client)
        schema = "year_month string, product_name string, total_revenue decimal(38, 2)"
        options = {"header": True}
        target_df = pp.io.read_csv_dataset(
            spark_client=spark_client,
            path="tests/integration/pipelines/top_revenue_target.csv",
            schema=schema,
            options=options,
        )

        # act
        pipeline.run()
        output_df = pp.io.read_csv_dataset(
            spark_client=spark_client,
            path="data/output/output.csv",
            schema=schema,
            options=options,
        )

        # assert
        pp.testing.assert_dataframe_equality(output_df=output_df, target_df=target_df)
