from enum import Enum

import typer
from sqlalchemy.future import Engine as _FutureEngine
from sqlmodel import SQLModel, create_engine

from pyspark_pipeline import pipelines
from pyspark_pipeline.core.env import get_database_url

app = typer.Typer()


def _build_engine() -> _FutureEngine:
    return create_engine(get_database_url())


@app.command()
def init_db() -> None:
    """Initialize the database with all models declared in domain."""
    SQLModel.metadata.create_all(_build_engine())


class PipelineEnum(str, Enum):
    """Possible choices for pipelines."""

    top_revenue = "top_revenue"
    sample = "sample"


MODEL_ENUM_MAP = {
    PipelineEnum.top_revenue: pipelines.TopRevenuePipeline,
    PipelineEnum.sample: pipelines.SamplePipeline,
}


@app.command()
def run(
    pipeline: PipelineEnum = typer.Option(PipelineEnum.top_revenue),
) -> None:
    """Trigger a pipeline ETL.

    Args:
        pipeline: choice of pipelines to run.

    """
    typer.echo("Instantiating pipeline ... ")
    pipeline_object = MODEL_ENUM_MAP[pipeline]()

    typer.echo("Running pipeline...")
    pipeline_object.run()
    typer.echo("Pipeline done!!!")


if __name__ == "__main__":
    app()
