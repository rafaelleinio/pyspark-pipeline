from pyspark_test.pipelines.top_revenue import TopRevenuePipeline


def main() -> None:
    pipeline = TopRevenuePipeline()
    pipeline.run()
    print(">>> Pipeline execution finished!!!")


if __name__ == "__main__":
    main()
