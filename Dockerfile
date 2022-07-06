FROM openjdk:8 as dependencies
COPY --from=python:3.10 / /

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY requirements.dev.txt .
RUN pip install --no-cache-dir -r requirements.dev.txt
COPY . .

FROM dependencies
RUN pip install .
