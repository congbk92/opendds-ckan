ARG BASIS=objectcomputing/opendds:latest
FROM $BASIS

COPY . /app
WORKDIR /app

RUN apt-get update && apt-get install -y \
    rapidjson-dev \
    python3-pip

RUN pip3 install -r requirements.txt

CMD python3 ./source/run.py
