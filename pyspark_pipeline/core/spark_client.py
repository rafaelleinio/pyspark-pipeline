"""SparkClient entity."""
from typing import Optional

from pyspark.sql import SparkSession


class SparkClient:
    """Handle Spark session connection."""

    def __init__(self, session: Optional[SparkSession] = None) -> None:
        self._session = session

    @property
    def session(self) -> SparkSession:
        """Get a created an SparkSession.

        Returns:
            Spark session.

        Raises:
            AttributeError: if the session is not created yet.

        """
        if not self._session:
            raise AttributeError("Please create session first.")
        return self._session

    def create_session(self) -> None:
        """Create or get a live Spark Session for the SparkClient.

        When creating the session the function installs all third-party packages
        dependencies. The first time installing, the session can take longer to be
        created, but the next times are faster.

        """
        if not self._session:
            self._session = (
                SparkSession.builder.appName("pyspark-pipeline")
                .config("spark.jars.packages", "org.postgresql:postgresql:42.4.0")
                .getOrCreate()
            )
            self._session.sparkContext.setLogLevel("ERROR")
