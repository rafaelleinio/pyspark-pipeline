from typing import Optional

from pyspark.sql import DataFrame, functions
from pyspark.sql.window import Window

from pyspark_test.core.io import read_csv_dataset, write_single_csv_dataset
from pyspark_test.core.pipeline import ETLPipeline
from pyspark_test.core.spark_client import SparkClient


class TopRevenuePipeline(ETLPipeline):
    """Top revenue etl pipeline implementation.

    This pipeline find the top revenue product by month.
    It will output a single csv file (output.csv) with the columns: year_month,
    product_name and total_revenue.

    """

    JOIN_QUERY = """
    SELECT
        products.product_id,
        products.product_name,
        sales.sale_date,
        sales.sale_price,
        sales.quantity
    FROM
        products
        JOIN sales ON products.product_id = sales.product_id
    """

    def __init__(self, spark_client: Optional[SparkClient] = None):
        super().__init__(spark_client)

    def _extract(self) -> DataFrame:
        # virtualize data sources
        read_csv_dataset(
            spark_client=self.spark_client,
            path="data/input/products.csv",
            options={"header": False},
            schema="product_id int, product_name string",
        ).createOrReplaceTempView("products")
        read_csv_dataset(
            spark_client=self.spark_client,
            path="data/input/sales.csv",
            options={"header": False},
            schema="product_id int, sale_date date, sale_price decimal(38, 2), "
            "quantity int",
        ).createOrReplaceTempView("sales")

        # merge input data
        return self.spark_client.session.sql(self.JOIN_QUERY)

    def _transform(self, df: DataFrame) -> DataFrame:
        add_columns_df = df.withColumn(
            "year_month",
            col=functions.expr(
                "concat(string(year(sale_date)), '-', string(month(sale_date)))"
            ),
        ).withColumn("total_price", col=functions.expr("sale_price * quantity"))

        agg_df = (
            add_columns_df.groupBy("year_month", "product_name")
            .agg(functions.sum(functions.col("total_price")).alias("total_revenue"))
            .select("year_month", "product_name", "total_revenue")
        )

        rank_df = (
            agg_df.withColumn(
                "rn",
                col=functions.row_number().over(
                    Window.partitionBy("year_month").orderBy(
                        functions.desc("total_revenue")
                    )
                ),
            )
            .where(condition="rn = 1")
            .select("year_month", "product_name", "total_revenue")
        )
        return rank_df

    def _load(self, df: DataFrame) -> None:
        write_single_csv_dataset(
            df=df,
            path="data/output/output.csv",
            order_by=["year_month"],
            options={"header": True},
        )
