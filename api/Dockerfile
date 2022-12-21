

FROM ubuntu:20.04

RUN apt-get update -y \
    && apt-get install -y software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get install openjdk-8-jdk -y \
    && apt-get install python3-pip -y \
    && export JAVA_HOME \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -q findspark

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/app

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
