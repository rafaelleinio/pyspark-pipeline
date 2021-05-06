from pyspark_test.core.testing import assert_dataframe_equality


def test_assert_dataframe_equality(spark_session):
    # arrange
    df1 = spark_session.sql("select 1 as id, 'a' as name")
    df2 = spark_session.sql("select 1 as id, 'a' as name")

    # act and assert
    assert_dataframe_equality(df1, df2)
