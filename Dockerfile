FROM rafaelleinio/docker-java-python

COPY ./requirements.txt /pyspark-test/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /pyspark-test/requirements.txt

COPY . /pyspark-test
RUN pip install /pyspark-test/.

WORKDIR /pyspark-test
CMD ["python", "./pyspark_test/pipelines/top_revenue_runner.py"]
