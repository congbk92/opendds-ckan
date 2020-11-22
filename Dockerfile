ARG BASIS=objectcomputing/opendds:latest
FROM $BASIS

COPY . /app
WORKDIR /app

RUN apt-get update && apt-get install -y \
    rapidjson-dev \
    python3

CMD python3 ./source/run.py