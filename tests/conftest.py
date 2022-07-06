import pytest

from pyspark_pipeline import SparkClient


@pytest.fixture
def spark_client(spark_session) -> SparkClient:
    return SparkClient(session=spark_session)
