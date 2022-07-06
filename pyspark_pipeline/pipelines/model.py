from typing import Optional

from sqlalchemy import Column
from sqlmodel import JSON, Field, SQLModel


class _SampleDatasetFieldGroupTwo(SQLModel):
    days_since_event: int
    key4: str
    key5: str


class _SampleDatasetFieldGroupOne(SQLModel):
    key1: str
    ke2: str
    key3: str


class _SampleDatasetRecord(SQLModel):
    field_group_one: _SampleDatasetFieldGroupOne
    field_group_two: _SampleDatasetFieldGroupTwo


class SampleDataset(SQLModel, table=True):
    """SampleDataset SQL Model."""

    __tablename__ = "sample_dataset"

    id: Optional[int] = Field(default=None, primary_key=True)
    version: str
    record: _SampleDatasetRecord = Field(sa_column=Column(JSON))
