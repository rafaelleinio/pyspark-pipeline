from unittest.mock import Mock

from pyspark.sql import DataFrame

from pyspark_test.core.pipeline import ETLPipeline


class DummyETLPipeline(ETLPipeline):
    def _extract(self) -> DataFrame:
        self.extract = 1
        return Mock(spec=DataFrame)

    def _transform(self, df: DataFrame) -> DataFrame:
        self.transform = 2
        return Mock(spec=DataFrame)

    def _load(self, df: DataFrame) -> None:
        self.load = 3


class TestETLPiepeline:
    def test_run(self):
        # arrange
        pipeline = DummyETLPipeline()

        # act
        pipeline.run()

        # assert
        assert pipeline.extract == 1
        assert pipeline.transform == 2
        assert pipeline.load == 3
