from fastapi import FastAPI, responses, Query

import pyspark
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext


app = FastAPI()


@app.get("/healthcheck")
def root():
    """check the api

    Returns:
        response: message telling if the api is running or not
    """
    return responses.JSONResponse(
        status_code=200, content={"message": "api is healthy!"}
    )


conf = (
    pyspark.SparkConf()
    .set("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1")
    .setMaster("local")
    .setAppName("myApp")
    .setAll([("spark.driver.memory", "40g"), ("spark.executor.memory", "50g")])
)

sc = SparkContext(conf=conf)


@app.get("/get_data")
def get_all_data():
    sql_cont = SQLContext(sc)

    mongo_ip = "mongodb://root:root@172.20.0.2:27017/test_db.Pacientes?authSource=admin"

    database = (
        sql_cont.read.format("com.mongodb.spark.sql.DefaultSource")
        .option("uri", mongo_ip)
        .load()
    )

    database.createOrReplaceTempView("Pacientes")

    data = sql_cont.sql("SELECT * FROM Pacientes")

    json_data = data.toPandas().to_json(orient="records")

    return responses.JSONResponse(status_code=200, content={"content": json_data})
