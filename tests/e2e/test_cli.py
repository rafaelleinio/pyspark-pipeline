from sqlmodel import Session
from typer.testing import CliRunner

from pyspark_pipeline import cli
from pyspark_pipeline.pipelines import model


def test_e2e_sample_pipeline():
    # arrange
    runner = CliRunner()

    # act and assert
    init_db_result = runner.invoke(cli.app, ["init-db"])
    assert init_db_result.exit_code == 0

    pipeline_result = runner.invoke(
        cli.app,
        [
            "run",
            "--pipeline",
            "sample",
        ],
    )
    assert pipeline_result.exit_code == 0

    with Session(cli._build_engine()) as session:
        count = session.query(model.SampleDataset).count()
    assert count == 1
