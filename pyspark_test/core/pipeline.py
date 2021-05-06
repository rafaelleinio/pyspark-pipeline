from abc import ABC, abstractmethod
from typing import Optional

from pyspark.sql import DataFrame

from pyspark_test.core.spark_client import SparkClient


class ETLPipeline(ABC):
    """Abstract class defining a simple ETL pipeline.

    Attributes:
        spark_client: client used to connect to Spark session.

    """

    def __init__(self, spark_client: Optional[SparkClient] = None):
        if not spark_client:
            spark_client = SparkClient()
            spark_client.create_session()
        self.spark_client = spark_client

    def run(self) -> None:
        """Run the pipeline.

        The ETLPipeline run method will orchestrate the extract, transform and load
        steps.

        """
        extract_df = self._extract()
        transform_df = self._transform(extract_df)
        return self._load(transform_df)

    @abstractmethod
    def _extract(self) -> DataFrame:
        """Materialization should implement extract step."""

    @abstractmethod
    def _transform(self, df: DataFrame) -> DataFrame:
        """Materialization should implement transform step."""

    @abstractmethod
    def _load(self, df: DataFrame) -> None:
        """Materialization should implement load step."""
