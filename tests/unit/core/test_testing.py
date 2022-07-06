import pytest

from pyspark_pipeline.core.testing import assert_dataframe_equality


def test_assert_dataframe_equality(spark_session):
    # arrange
    df1 = spark_session.sql("select 1 as id, 'a' as name")
    df2 = spark_session.sql("select 1 as id, 'a' as name")

    # act and assert
    assert_dataframe_equality(df1, df2)


def test_assert_dataframe_equality_shape_mismatch(spark_session):
    # arrange
    df1 = spark_session.sql("select 1 as id, 'a' as name")
    df2 = spark_session.sql("select 1 as id")

    # act and assert
    with pytest.raises(AssertionError):
        assert_dataframe_equality(df1, df2)


def test_assert_dataframe_equality_different_values(spark_session):
    # arrange
    df1 = spark_session.sql("select 1 as id")
    df2 = spark_session.sql("select 2 as id")

    # act and assert
    with pytest.raises(AssertionError):
        assert_dataframe_equality(df1, df2)


def test_assert_dataframe_equality_not_df(spark_session):
    # arrange
    df1 = None
    df2 = spark_session.sql("select 2 as id")

    # act and assert
    with pytest.raises(AssertionError):
        assert_dataframe_equality(df1, df2)
