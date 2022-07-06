from setuptools import find_packages, setup

__package_name__ = "pyspark_pipeline"
__version__ = "1.0.0"
__repository_url__ = "https://github.com/rafaelleinio/pyspark-test"

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name=__package_name__,
    version=__version__,
    url=__repository_url__,
    packages=find_packages(
        exclude=["tests", "pipenv", "env", "venv", "htmlcov", ".pytest_cache", "pip"]
    ),
    license="MIT",
    author="Rafael Leinio",
    description="Data quality and profiling tool powered by Apache Spark.",
    keywords="apache-spark pyspark pipeline",
    install_requires=requirements,
    entry_points="""
    [console_scripts]
    pcli=pyspark_pipeline.cli:app
    """,
)
