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

        When creating the session the function installs the Graphframes extension if not
        presented.

        """
        if not self._session:
            self._session = SparkSession.builder.appName("meli-challenge").getOrCreate()
            self._session.sparkContext.setLogLevel("ERROR")
