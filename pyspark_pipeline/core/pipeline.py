from abc import ABC, abstractmethod
from typing import Optional

from pyspark.sql import DataFrame

from pyspark_pipeline.core.spark_client import SparkClient


class ETLPipeline(ABC):
    """Abstract class defining a simple ETL pipeline.

    Attributes:
        spark_client: client used to connect to Spark session.

    """

    def __init__(self, spark_client: Optional[SparkClient] = None):
        self.spark_client = spark_client or SparkClient()

    def run(self) -> None:
        """Run the pipeline.

        The ETLPipeline run method will orchestrate the extract, transform and load
        steps.

        """
        self.spark_client.create_session()
        extract_df = self._extract()
        transform_df = self._transform(extract_df)
        return self._load(transform_df)

    @abstractmethod
    def _extract(self) -> DataFrame:
        """Child class should implement extract step."""

    @abstractmethod
    def _transform(self, df: DataFrame) -> DataFrame:
        """Child class should implement transform step."""

    @abstractmethod
    def _load(self, df: DataFrame) -> None:
        """Child class should implement load step."""
